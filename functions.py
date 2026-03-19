import os

from alive_progress import alive_bar

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure

from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.integrate import quad,IntegrationWarning

from os.path import isfile,isdir

################################################################################
################################ VARIBALES #####################################

start_level_column=0 
stalc_name='LevelLITERATURE'

primary_column = 5
pc_name = 'Primary?'

gamma_ray_energy_column = 6
grec_name='Egamma-LITERATURE'

stop_level_column = 8
stplc_name='Level_final'

spectra_directory=os.path.join(os.getcwd(),'spectra')

################################ END VARIABLES #################################
################################################################################

################################################################################
################################ FUNCTIONS #####################################

def LoadToBeSkipped(_filename:str):
    _gammaray_to_be_skipped = np.genfromtxt(_filename,dtype=float,delimiter=',')
    return _gammaray_to_be_skipped


def LoadLevelScheme(_filename) -> pd.DataFrame:
    '''

    LoadLevelScheme(): load the excel file named '_filename' into a pandas
    dataFrame using the columns and their names defined at the beginning
    of the code in the VARIBALES section.
    This function is EXTREMELY SLOW if used on an Excel file with multpile
    sheets. Best practice is to use a csv file or a excel file with just 
    1 single sheet.

        Input: - (_filename) name of the file to load

        Returns: - (_lvlScheme) a DataFrame containing loaded data from 
                    _filename.
                 - (_loading_time) time needed to load _filename.

    '''
    print('Loading ...')
    _lvlScheme=pd.read_excel(_filename,
                            sheet_name='44Ca Level scheme',
                            usecols=[start_level_column,primary_column,
                                        gamma_ray_energy_column,
                                        stop_level_column],
                            dtype={stalc_name: 'float',pc_name:'str',
                                   grec_name: 'float',stplc_name: 'float'})
    _lvlScheme.reset_index()

    return _lvlScheme


def Gauss(_x,_mean,_sigma,_amplitude) -> np.ndarray:
    ''' 

    Gauss(): is a gaussian function that calculates the energy
    corresponding to x (x can be array-like)

    '''

    return np.asarray(_amplitude * np.exp(-(_x-_mean)**2/(2*_sigma**2)))


def GaussPol1(_x,_mean,_sigma,_amplitude,_m,_q) -> np.ndarray:
    ''' 

    GaussPol1(): is a gaussian function + a degree 1 polinomial that
    calculates the energy corresponding to x (x can be array-like)

    '''
    
    return np.asarray(Gauss(_x,_mean,_sigma,_amplitude) + _m*_x + _q)


def FitGauss(_hist,_init_parameters,_limit=[0,-1]):
    ''' 

    FitGauss(): As name suggests, this function do a gaussian fit of a
    given histogram (hist).

        Inputs: - (_hist) the histogram 
                - (_init_parameters) first guess
                  of the parameters for the fitting function (curve_fit).

        Returns: - (_best_parameters) the best parameters found with
                    curve_fit.
                 - (_cov) covariance matrix of the best parameters
                 - (_I) the sum of the bin contents inside the fit region
                 - (_I_diff) the difference between (_I) and the integral
                    of the function calculate inside (_limit). This value is
                    extremely helpfull to understand if a fit is good or not
                 - zero for everything and 1000000000 for (_I_diff) if
                    curve_fit cannot converge.

    '''
    _lower,_upper=_limit
    _lower=int(_lower)
    _upper=int(_upper)

    try:

        _best_parameters,_cov=curve_fit(GaussPol1,
                                 _hist[_lower:_upper,0],
                                 _hist[_lower:_upper,1],
                                 p0=_init_parameters,
                                 bounds=([0,0,0,-np.inf,-np.inf],
                                         [np.inf,np.inf,np.inf,np.inf,np.inf]))
        _I_hist=np.sum(_hist[_lower:_upper,1])
        _I_fit=quad(GaussPol1,_lower,_upper,args=tuple(_best_parameters))[0]
        _I_diff=int(_I_fit-_I_hist)
        _I=quad(Gauss,_lower,_upper,args=tuple(_best_parameters[0:3]))[0]

    except:

        _I=0
        _I_diff=1000000000
        _best_parameters=[0,0,0,0,0]
        _cov=[[0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]]

    return [_best_parameters,_cov,_I_diff,_I]


def DrawFitResults(_hist,_level_directory:str,_gate_energy:float,_peak:float,
                   _limit:list[int],_results,_show_flag:bool=0) ->list[
                                            matplotlib.figure.Figure,plt.Axes]:

    '''

    DrawFitResults():   draw the hist area inside [_limit] and the fit
                        corresponding to _results.
    
        Inputs: - (_hist) the histogram to draw
                - (_level_directory) level energy to set the title
                - (_gate_energy)(float) gate energy to set the title
                - (_peak)(float) peak energy to set the title
                - (_limit)(int,int) lower and upper limit to draw the histogram
                  and the fit.
                - (_results) gaussian function parameters
                - (_show_flag)(bool) this flag is used to suppres the plt.show()
                  function when running SAURON wiht --run-all option.

    '''
    _lower,_upper=_limit
    _lower=int(_lower)
    _upper=int(_upper)
    _parameters,*_=_results
    _fig,_ax=plt.subplots(1,1,figsize=(7,3))
    _energy_axis=np.linspace(_lower,_upper,500)
    _ax.set_title(f'LEVEL: {_level_directory.replace('/','')}'
                  +f' # GATE: {_gate_energy}'
                  +f' # TRANSITION: {_peak}')
    _ax.bar(_hist[_lower:_upper,0],_hist[_lower:_upper,1])
    _ax.plot(_energy_axis,
             GaussPol1(_energy_axis,*_parameters),
             color='darkorange')
    if _show_flag:
        plt.show()
    plt.close()

    return _fig,_ax


def SaveFitResults(_level_directory:str,_gate_energy:float,_peak:float,
                   _results,_stop_level:float):
    '''
    SaveFitResults(): function that save the fit results on the appropriate
    output file.
    It is called every time a fit is performed and, if SAURON, is called in
    single-peak mode, it asks the user if they want to store the results.
    The answer is valide also for the fit .png image.

        Inputs: - (_level_directory) directory where to save the output file.
                - (_gate_energy) energy of the gate used to set the
                  the output filename.
                - (_peak) energy of the peak used to set the output filename
                - (_results) results of the fit to be printed on the output
                  file.
    '''
    os.chdir(spectra_directory)
    _output_filename=os.path.join(_level_directory,
                                  str(_gate_energy)+'-'+str(_peak)+'.out.txt')
    _best_parameters,_cov,_I_diff,_I=_results
    with open(_output_filename,'w') as _f:
        print('START LEVEL,STOP LEVEL,Integral Diff,Integral,TRANSITION,GATE,'
               +'mean,fwhm,amplitude,m,q,'
               +'err_mean,err_fwhm,err_amplitude,err_m,err_q',
              file=_f)
        print(f'{float(_level_directory.replace('/',''))}',
              f'{_stop_level}',
              f'{_I_diff:.4f}',
              f'{_I:.4f}',
              f'{_peak:.4f}',
              f'{float(_gate_energy):.4f}',
              f'{_best_parameters[0]:.4f}',
              f'{_best_parameters[1]*2.355:.4f}', # Saving fwhm instead of 
              f'{_best_parameters[2]:.4f}',       # sigma to be consistent
              f'{_best_parameters[3]:.4f}',       # with Cubix fit results
              f'{_best_parameters[4]:.4f}',
              f'{np.sqrt(_cov[0][0]):.4f}',
              f'{np.sqrt(_cov[1][1])*2.355:.4f}',
              f'{np.sqrt(_cov[2][2]):.4f}',
              f'{np.sqrt(_cov[3][3]):.4f}',
              f'{np.sqrt(_cov[4][4]):.4f}',
              sep=',',
              file=_f)


def SaveFigReuslts(_level_directory:str,_gate_energy:float,_peak:float,
                   _fig:matplotlib.figure.Figure,_ax:plt.Axes):
    '''

    SaveFigReuslts(): just a wrap for plt.savefig()

    '''
    _fig.savefig(os.path.join(_level_directory,
                              str(_gate_energy)+'-'+str(_peak)+'.png'),dpi=300)


def FitSinglePeak(_level_scheme:pd.DataFrame,_level_directory:float,
                  _gate_energy:float,_peak:float,_param=None,
                  _limit:list[int]=None,_called_directly:bool=0):
    '''

    FitSinglePeak(): wrap FitGauss() and runs it for the one selected peak.
                    if it doesn't find the right file it returns -1000 as
                    result.

        Inputs: - (_level_scheme) a pandas dataFrame with the entire level
                  level scheme stored inside.
                - (_level_directory) directory containing the .dat file of a
                  specific pair of gate and gamma ray.
                - (_gate_energy) energy of the gate.
                - (_peak) energy of the peak to fit.
                - (_param) initial guess of the fit parameters.
                - (_limit) upper and lower limit of the fiting region.
                - (_called_directly) this is a flag to check if the user is
                  doing a single fit (in this case the main() will call
                  this function directly) or if they are doing more than
                  one fit (in this case the main() will call thi function
                  from inside FitSingleLevel() or from inside 
                  FitEntireLevelScheme().

        Returns: - (_reuslts) results of the FitGauss() function call.

    '''
    # Find the energy level populated by _peak
    mask1=_level_scheme[grec_name]==float(_peak)
    mask2=_level_scheme[stalc_name]==float(_level_directory)
    _stop_level=float(_level_scheme[mask1 & mask2][stplc_name].values[0])
    _start_level=float(_level_scheme[mask1 & mask2][stalc_name].values[0])

    # Move into the right directory and upload the gammaray spectra gated on
    # the _gate_energy
    os.chdir(spectra_directory)
    _level_directory=os.path.join(str(_level_directory),'')
    _filename=str(_gate_energy)+'.dat'
    if os.path.isfile(_level_directory+_filename):
        _hist=np.genfromtxt(_level_directory+_filename)
    else:
        _results=-10000 
        return _results

    # Check if the user passed _param and _limit from the command line
    if _param==None: _param=[_peak,2,_hist[int(_peak),1],-0.1,10]
    if _limit==None: _limit=[_peak-20,_peak+20]

    # Perform the fit
    _results=FitGauss(_hist,_param,_limit)

    # Print results but only if called directly by the user (this is done to
    # prevent annoying printing when running multiple recursive fits)
    if _called_directly:
        try:
            print('\n')
            print(f'LEVEL: {_level_directory.replace('/','')}  GATE: {_gate_energy}  TRANSITION: {_peak}')
            print(f'Fit Results --------------------------------------------------------\n \
                    Mean:      {float(_results[0][0]):10.3} +- {np.sqrt(float(_results[1][0][0])):10.3}\
            | {np.sqrt(float(_results[1][0][0]))/float(_results[0][0]):5.0%}\n \
                    Sigma:     {float(_results[0][1]):10.3} +- {np.sqrt(float(_results[1][1][1])):10.3}\
            | {np.sqrt(float(_results[1][1][1]))/float(_results[0][1]):5.0%}\n \
                    Amplitude: {float(_results[0][2]):10.3} +- {np.sqrt(float(_results[1][2][2])):10.3}\
            | {np.sqrt(float(_results[1][2][2]))/float(_results[0][2]):5.0%}\n \
                    m:         {float(_results[0][3]):10.3} +- {np.sqrt(float(_results[1][3][3])):10.3}\
            | {np.sqrt(float(_results[1][3][3]))/float(_results[0][3]):5.0%}\n \
                    q:         {float(_results[0][4]):10.3} +- {np.sqrt(float(_results[1][4][4])):10.3}\
            | {np.sqrt(float(_results[1][4][4]))/float(_results[0][4]):5.0%}\n \
                    I_diff:    {float(_results[2]):10.3}\n \
                    I:         {float(_results[3]):10.3}\n '+
                    '           --------------------------------------------------------\n')
        except:
            print('\n')
            print(f'LEVEL: {_level_directory.replace('/','')}  GATE: {_gate_energy}  TRANSITION: {_peak}')
            print(f'Fit Results --------------------------------------------------------\n \
                    Mean:      {float(_results[0][0]):10.3} +- {np.sqrt(float(_results[1][0][0])):10.3}\n \
                    Sigma:     {float(_results[0][1]):10.3} +- {np.sqrt(float(_results[1][1][1])):10.3}\n \
                    Amplitude: {float(_results[0][2]):10.3} +- {np.sqrt(float(_results[1][2][2])):10.3}\n \
                    m:         {float(_results[0][3]):10.3} +- {np.sqrt(float(_results[1][3][3])):10.3}\n \
                    q:         {float(_results[0][4]):10.3} +- {np.sqrt(float(_results[1][4][4])):10.3}\n \
                    I_diff:    {float(_results[2]):10.3}\n \
                    I:         {float(_results[3]):10.3}\n '+
                    '           --------------------------------------------------------\n')
 
    # Draw the results and check if the user wants to save 'em.
    # If the function is called from FitSingleLevel (_called_directly=0) then
    # the results are automaticaly saved.
    _fig,_ax=DrawFitResults(_hist,_level_directory,_gate_energy,_peak,_limit,
                            _results,_show_flag=_called_directly)

    if _called_directly==1:
        if choice:=input('Do you want to save the results? [Y/n] ')!='n':
            SaveFitResults(_level_directory,_gate_energy,_peak,_results,_stop_level)
            SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax)
        else:
            pass
    else:
        SaveFitResults(_level_directory,_gate_energy,_peak,_results,_stop_level)
        SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax)


    return _results


def FitSinglePrimaryPeak(_level_scheme:pd.DataFrame,_level_directory:str,
                         _gammaray_energy:float,
                         _secondary_gammaray_energy:float,_gate_directory:float,
                         _param:list[float]=None,_limit:list[int]=None,
                         _called_directly:bool=0):
    '''

    FitSinglePrimaryPeak(): wrap FitGauss() and runs it for the one selected
        primary peak.
    
        Inputs: - (_level_scheme) a pandas dataFrame with the entire level
                  level scheme stored inside.
                - (_level_directory) directory to store the file in namely,
                  the binding level directory
                - (_gammaray_energy) energy of the peak to fit
                - (_secondary_gammaray_energy) energy of the gate
                - (_param) initial guess of the fit parameters.
                - (_limit) upper and lower limit of the fiting region.
                - (_called_directly) this is a flag to check if the user is
                  doing a single fit (in this case the main() will call
                  this function directly) or if they are doing more than
                  one fit (in this case the main() will call thi function
                  from inside FitBindingLevel() or from inside 
                  FitEntireLevelScheme().

        Returns: - (_reuslts) results of the FitGauss() function call.

    '''
    # Move into the directory containing the gate spectra and upload the gated
    # file.
    mask=_level_scheme[grec_name]==_gammaray_energy
    _primary_level_scheme=_level_scheme[mask].reset_index(drop=True)
    os.chdir(os.path.join(spectra_directory,str(_gate_directory)))
    _hist=np.genfromtxt(str(_secondary_gammaray_energy)+'.dat')
    _peak=_gammaray_energy
    _gate_energy=_secondary_gammaray_energy
    _stop_level=float(_level_scheme[(_level_scheme[grec_name]==float(_peak)) 
        & (_level_scheme[stalc_name]==float(_level_directory))][stplc_name].values[0])

    # Check if the user passed _param and _limit from the command line
    if _param==None: _param=[_peak,2,_hist[int(_peak),1],-0.1,10]
    if _limit==None: _limit=[_peak-20,_peak+20]
    _results=FitGauss(_hist,_param,_limit)

    # Draw the results and check if the user wants to save 'em.
    # If the function is called from FitBindingLevel (_called_directly=0) then
    # the results are automaticaly saved.
    if _called_directly:
        try:
            print('\n')
            print(f'Fit Results --------------------------------------------------------\n \
                    Mean:      {float(_results[0][0]):10.3} +- {np.sqrt(float(_results[1][0][0])):10.3}\
            | {np.sqrt(float(_results[1][0][0]))/float(_results[0][0]):5.0%}\n \
                    Sigma:     {float(_results[0][1]):10.3} +- {np.sqrt(float(_results[1][1][1])):10.3}\
            | {np.sqrt(float(_results[1][1][1]))/float(_results[0][1]):5.0%}\n \
                    Amplitude: {float(_results[0][2]):10.3} +- {np.sqrt(float(_results[1][2][2])):10.3}\
            | {np.sqrt(float(_results[1][2][2]))/float(_results[0][2]):5.0%}\n \
                    m:         {float(_results[0][3]):10.3} +- {np.sqrt(float(_results[1][3][3])):10.3}\
            | {np.sqrt(float(_results[1][3][3]))/float(_results[0][3]):5.0%}\n \
                    q:         {float(_results[0][4]):10.3} +- {np.sqrt(float(_results[1][4][4])):10.3}\
            | {np.sqrt(float(_results[1][4][4]))/float(_results[0][4]):5.0%}\n \
                    I_diff:    {float(_results[2]):10.3}\n \
                    I:         {float(_results[3]):10.3}\n '+
                    '           --------------------------------------------------------\n')
        except:
            print('\n')
            print(f'Fit Results --------------------------------------------------------\n \
                    Mean:      {float(_results[0][0]):10.3} +- {np.sqrt(float(_results[1][0][0])):10.3}\n \
                    Sigma:     {float(_results[0][1]):10.3} +- {np.sqrt(float(_results[1][1][1])):10.3}\n \
                    Amplitude: {float(_results[0][2]):10.3} +- {np.sqrt(float(_results[1][2][2])):10.3}\n \
                    m:         {float(_results[0][3]):10.3} +- {np.sqrt(float(_results[1][3][3])):10.3}\n \
                    q:         {float(_results[0][4]):10.3} +- {np.sqrt(float(_results[1][4][4])):10.3}\n \
                    I_diff:    {float(_results[2]):10.3}\n \
                    I:         {float(_results[3]):10.3}\n '+
                    '           --------------------------------------------------------\n')

    _fig,_ax=DrawFitResults(_hist,_level_directory,_gate_energy,_peak,_limit,
                            _results,_show_flag=_called_directly)

    if _called_directly==1:
        if choice:=input('Do you want to save the results? [Y/n] ')!='n':
            SaveFitResults(_level_directory,_gate_energy,_peak,_results,_stop_level)
            SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax)
    else:
        SaveFitResults(_level_directory,_gate_energy,_peak,_results,_stop_level)
        SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax)


def FitSingleLevel(_level_scheme:pd.DataFrame,_gammaray_to_be_skipped,
                   _level_directory:str,_called_directly:bool=0):
    '''

    FitSingleLevel(): wrap FitGauss() and runs it for the one selected level.
    
        Inputs(): - (_level_scheme) the pandas dataFrame containing the level
                    scheme.
                  - (_level_directory) the directory to be analysed.

    '''
    os.chdir(spectra_directory)
    _energy_level=float(_level_directory)
    _subset_level_scheme_mask=_level_scheme[stalc_name]==_energy_level
    _subset_level_scheme=_level_scheme[_subset_level_scheme_mask].reset_index(drop=True)
    #print(f'Now working on: {_level_directory}')
    for _filename in os.listdir(_level_directory):
        if _filename.endswith('.dat'):
            _gate_energy=_filename.replace('.dat','')
            _filename=os.path.join(_level_directory,_filename)
            for _index,_gammaray in _subset_level_scheme.iterrows():
                # Check if the pair (_gammaray,_gate) needs to be skipped
                if((_gammaray[grec_name],float(_gate_energy)) in _gammaray_to_be_skipped):
                    pass
                else:
                    _peak=_gammaray[grec_name]
                    _results,*_=FitSinglePeak(_level_scheme,
                                              _level_directory,
                                              _gate_energy,
                                              _peak,
                                              _called_directly=_called_directly)


def FitBindingLevel(_level_scheme:pd.DataFrame,_gammaray_to_be_skipped,
                    _called_directly:bool=0):
    '''

    FitBindingLevel(): wrap FitGauss() and runs it for the capture level.
 
        Inputs(): - (_level_scheme) the pandas dataFrame containing the level
                    scheme.

    '''

    os.chdir(spectra_directory) #così mi trovo dentro la cartella spectra/. 
    mask=_level_scheme[pc_name]=='YES'
    _primary_level_scheme=_level_scheme[mask].reset_index(drop=True)      

    for _index,_primary_gammaray in _primary_level_scheme.iterrows():
        _ending_level=_primary_gammaray[stplc_name]
        mask1=_level_scheme[stalc_name]==_ending_level
        for _secondary_index,_secondary_gammaray in _level_scheme[mask1].iterrows():
            # Check if the pair (_gammaray,_gate) needs to be skipped
            if((_primary_gammaray[grec_name],float(_secondary_gammaray[grec_name])) 
                   in _gammaray_to_be_skipped):
                pass
            else:
                FitSinglePrimaryPeak(_level_scheme,
                                    str(_primary_gammaray[stalc_name]),
                                    _primary_gammaray[grec_name],
                                    _secondary_gammaray[grec_name],
                                    _secondary_gammaray[stplc_name],
                                    _param=None,
                                    _limit=None,
                                    _called_directly=_called_directly)


def FitSpecial(_level_scheme:pd.DataFrame):
    '''
        
        FitSpecial(): read the single-spectra file and performs the fits of
        every special casefollowing the condition specified for each one 
        directly inside the file.
        FitSpecial is not a fancy function. It performs a line-by-line reading
        of the single-spectra file. Each line is saved as a string and the
        program will look for in-line conditions like -g -d -p and so on.
    
            Inputs(): - (_level_scheme) the pandas dataFrame containing the 
                        level scheme.

    '''
    special_file = 'single-spectra.txt'

    with open(special_file,'r') as file:
        for line in file:
            _level_directory=line.split('-d ')[1].split('-')[0].replace(' ','')
            _gate_energy=line.split('-g ')[1].split('-')[0].replace(' ','')
            _gammaray_energy=float(line.split('-p ')[1].split('-')[0].replace(' ',''))
            _gate_directory=line.split('-gd ')[1].split('-')[0].replace(' ','') if '-gd' in line else None
            _limit=[float(elem) for elem in line.split('--limit')[1].split('-')[0].split(' ')[1:3]] if '--limit' in line else None
            _param=[float(elem) for elem in line.split('--param')[1].split(' ')[1:6]] if '--param' in line else None
            _called_directly=0 if '--dont-ask' in line else 1# Da modifica qui ci va uno zero 

            if '--primary' in line:
                FitSinglePrimaryPeak(_level_scheme,_level_directory,
                                     _gammaray_energy,_gate_energy,
                                     _gate_directory,_param,_limit,
                                     _called_directly)
            else:
                FitSinglePeak(_level_scheme,_level_directory,_gate_energy,
                              _gammaray_energy,_param,_limit,_called_directly)


def FitEntireLevelScheme(_level_scheme:pd.DataFrame,
                         _gammaray_to_be_skipped):
    '''

        FitEntireLevelScheme(): call FitSingleLevel() on every level directory
        present inside the spectra/ folder.
    
            Inputs(): - (_level_scheme) the pandas dataFrame containing the 
                        level scheme.

    '''
    # Call the FitSingleLevel() function for every directory found inside the
    # spectra directory and then call FitBindingLevel.
    # As the code is extremely stupid, it will run the FitSingleLevel also on
    # the capture level directory, but this shouldn't be a problem since it 
    # won't find any gammaray populating the capture state, and thus it will
    # skipp everything.
    # After that also the capture state will be analysed by the call to the
    # function FitBindingLevel().
    # The last step is the fit of all special cases contained inside the
    # single-spectra file
    os.chdir(spectra_directory)
    with alive_bar(len(os.listdir())) as bar:
        for _level_directory in os.listdir():
            if isdir(_level_directory):
                FitSingleLevel(_level_scheme,_gammaray_to_be_skipped,
                               _level_directory,_called_directly=0)
            bar()
    with alive_bar(2) as bar:
        FitBindingLevel(_level_scheme,_gammaray_to_be_skipped)
        bar()
        FitSpecial(_level_scheme)
        bar()

################################ FUNCTIONS #####################################
################################################################################


