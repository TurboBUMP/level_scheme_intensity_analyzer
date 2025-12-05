#!/usr/bin/python3

# Check gamma-ray intensity balance of a level-scheme loaded on an excel file 
# containing all the transitions of a nucleus.
# 
# To use SAURON you need to specify if you want to run the fitting function
# only on one single peak, on an entire single level or on the entire level
# scheme.
# To do so you can:
#   ./sauron.py --redo-all
#   ./sauron.py --single-level -d <folder>
#   ./sauron.py -d <folder> -g <gate-energy>  -p <peak-energy> --param <parameters> --limit <limits>
#
#
# Keep in mind that SAURON expects a directory named spectra/ containing all 
# the subdirectories with the gated energy histograms. 
# The directory-tree must be structured as follows:
# 
# --> <dir-spectra/>
#
#   --> <dir_1/>
#           gate_energy_1.dat
#           gate_energy_2.dat
#
#   --> <dir_2/>
#           gate_energy_3.dat
#           gate_energy_4.dat
#
# <dir> name must match the energy of the level (precisely): 
# Example: directory 1157.0208 contains all file .dat relative to that level
#
# The excel file must contain three columns stating for each transition: 
# [start level, gamma ray energy, stop level]
# The first line must contain the name of each column to let Pandas be able to 
# initialise the dataFrame properly. 
# 
# Example: 
#       _start_level_colum = 1 
#       _gamma_ray_energy_column = 2
#       _stop_level_column = 3
#
# Here after you can specify you own columns number and the name of each column
#

start_level_colum = 0 
stalc_name='LevelLITERATURE'

primary_colum = 4
pc_name = 'Primary?'

gamma_ray_energy_column = 5
grec_name='Egamma-LITERATURE'

stop_level_column = 7
stplc_name='Level_final'

spectra_directory='/home/massimiliano/Desktop/Mordor/spectra/'

# 'gammaray_to_be_skipped' is a list of pairs that stores all the pairs of 
# gate-and-spectra that (for some reasons) need to be skipped.
# Each pair should be inserted as (gammaray_energy, gate_energy)
gammaray_to_be_skipped = [(1157.004,4932.8),
                          (1126.078,3731.0),
                          (2656.44,2435.3),
                          (1417.0,475.2),
                          (1417.0,894.2),
                          (1417.0,1107.98),
                          (1417.0,1582.8),
                          (1417.0,1995.8),
                          (1417.0,2291.4),
                          (263.53,1244.75),
                          (263.53,1276),
                          (263.53,1494.6),
                          (651.353,1575.9),
                          (263.53,1788.5),
                          (263.53,1989.17),
                          (651.353,1989.17),
                          (263.53,2033.8),
                          (1024.738,2033.8),
                          (263.53,2088),
                          (651.353,2150.9),
                          (263.53,2150.9),
                          (263.53,2193.2),
                          (263.53,3672.8),
                          (1024.738,605.8),
                          (263.53,887.5),
                          (2200.1,2037.9),
                          (1074.13,556.8),
                          (2200.1,556.8),
                          (2540.39,1141.1),
                          (1777.973,1839.7),
                          (368.208,1420.2),
                          (1017.5,1825.9),
                          (368.208,2534.7),
                          (1017.5,2534.7),
                          (368.208,519.7),
                          (1017.5,519.7),
                          (667.3,1384.4),
                          (2554.9,1384.4),
                          (667.3,1518.2),
                          (2554.9,1518.2),
                          (667.3,1577.4),
                          (2554.9,1577.4),
                          (667.3,1588.7),
                          (667.3,1683.4),
                          (667.3,1836.6),
                          (2554.9,1836.6),
                          (667.3,202.1),
                          (2554.9,2063.2),
                          (667.3,211.3),
                          (404.26,211.3),
                          (2554.9,211.3),
                          (667.3,2154.6),
                          (2554.9,2154.6),
                          (667.3,2223.1),
                          (2554.9,2223.1),
                          (667.3,2282.2),
                          (2554.9,2282.2),
                          (2554.9,2499),
                          (2554.9,2957.6),
                          (667.3,3138.4),
                          (2554.9,3138.4),
                          (667.2,646.5),
                          (2554.9,646.5),
                          (667.3,7418.8),
                          (2554.9,7418.8),
                          (3775.3,1250.2),
                          (1119.7,1520.2),
                          (475.2,1524.4),
                          (1119.7,1524.4),
                          (3775.3,1524.4),
                          (475.2,1771.9),
                          (3775.3,1771.9),
                          (3775.3,1816.3),
                          (475.2,1816.3),
                          (1119.7,1816.3),
                          (3775.3,1998.6),
                          (1119.7,2896.7),
                          (3775.3,2896.7),
                          (475.2,703.4),
                          (1119.7,703.4),
                          (3775.3,703.4),
                          (869.47,1374.8),
                          (556.8,1658.8),
                          (605.8,1819.3),
                          (556.8,1819.3),
                          (556.8,1860.2),
                          (605.8,1860.2),
                          (202.1,1860.2),
                          (202.1,1867.4),
                          (556.8,1867.4),
                          (556.8,2178.6),
                          (556.8,2297.5),
                          (202.1,2758.5),
                          (556.8,2758.5),
                          (202.1,651.07),
                          (1630.4,651.07),
                          (202.1,670.4),
                          (556.8,670.4),
                          (605.8,670.4),
                          (1630.4,670.4),
                          (211.3,1419.3),
                          (211.3,2289.2),
                          (211.3,2746.5),
                          (299.5,1491.1),
                          (299.5,2662),
                          (1727.5,2969.2),
                          (4196.1,1093.2),
                          (887.5,1093.2),
                          (1912.18,1101.3),
                          (4196.1,1101.3),
                          (483.4,1101.3),
                          (894.2,1101.3),
                          (4196.1,1212.5),
                          (887.5,1212.5),
                          (894.2,1212.5),
                          (1538.8,1212.5),
                          (894.2,1353.1),
                          (483.4,1353.1),
                          (4196.1,1353.1),
                          (894.2,1397.4),
                          (519.7,1397.4),
                          (483.4,1397.4),
                          (4196.1,1397.4),
                          (1912.18,1397.4),
                          (1538.8,1397.4),
                          (1538.8,1537.8),
                          (1912.18,1537.8),
                          (4196.1,1537.8),
                          (483.4,1537.8),
                          (519.7,1537.8),
                          (887.5,1537.8),
                          (894.2,1537.8),
                          (519.7,1579.6),
                          (4196.1,1579.6),
                          (894.2,2477.0),
                          (887.5,2477.0),
                          (519.7,2477.0),
                          (483.4,2477.0),
                          (4196.1,2477.0),
                          (519.7,6935.2),
                          (483.4,6935.2),
                          (894.2,900.8),
                          (887.5,900.8),
                          (519.7,900.8),
                          (4196.1,900.8),
                          (1538.8,900.8),
                          (1007.7,1277.6),
                          (1007.7,1418.1),
                          (1007.7,1619.6),
                          (646.5,1142.9),
                          (682.34,1142.9),
                          (1701.9,1142.9),
                          (1314.1,1142.9),
                          (682.34,1416.7),
                          (646.5,1416.7),
                          (682.34,2313.6),
                          (646.5,2313.6),
                          (1314.1,2313.6),
                          (646.5,2491.7),
                          (1701.9,2491.7),
                          (1314.1,2491.7),
                          (722.6,1194.1),
                          (686.9,1335.0),
                          (1091.1,1335.0),
                          (722.6,1691.6),
                          (2115.5,1691.6),
                          (722.6,2451.1),
                          (747.63,1183.5),
                          (3252.07,1183.5),
                          (733.0,1183.5),
                          (1107.98,1183.5),
                          (733.0,1324.0),
                          (747.63,1324.0),
                          (747.63,6721.0),
                          (733.0,6721.0),
                          (1107.98,6721.0),
                          (703.4,1113.6),
                          (2596.1,1113.6),
                          (703.4,171.3),
                          (2596.1,171.3),
                          (703.4,6651.3),
                          (670.4,1455.1),
                          (1283.4,1455.1),
                          (1276.0,1455.1),
                          (1207.2,532.1),
                          (670.4,1191.2),
                          (670.4,1626.8),
                          (4582.0,1626.8),
                          (1283.4,1626.8),
                          (1226.9,1626.8),
                          (4582.0,2088.2),
                          (670.4,2088.2),
                          (4582.0,645.7),
                          (1539.4,704.5),
                          (4582.0,704.5),
                          (1226.9,704.5),
                          (989.0,6480.2),
                          (1342.8,898.0),
                          (171.3,898.0),
                          (874.3,898.0),
                          (974.4,898.0),
                          (989.0,898.0),
                          (2145.52,6328.3),
                          (1494.6,6328.3),
                          (1141.1,6328.3),
                          (1494.6,972.6),
                          (2145.52,972.6),
                          (1141.1,972.6),
                          (2919.1,972.6),
                          (4801.7,972.6),
                          (1222.5,1050.9),
                          (1582.8,1050.9),
                          (1524.2,1050.9),
                          (2722.4,496.4),
                          (1961.0,496.4),
                          (1961.0,727.2),
                          (3848.9,727.2),
                          (532.1,1753.1),
                          (900.8,1753.1),
                          (1384.4,1753.1),
                          (1173.9,1753.1),
                          (900.8,476.8),
                          (697.6,476.8),
                          (532.1,476.8),
                          (1420.2,476.8),
                          (1384.4,476.8),
                          (532.1,678.6),
                          (2052.1,678.6),
                          (1420.2,678.6),
                          (1173.9,678.6),
                          (1844.7,1017.0),
                          (3973.1,1017.0),
                          (645.7,545.3),
                          (1518.2,545.3),
                          (1922.4,545.3),
                          (1196.7,444.5),
                          (1366.1,444.5),
                          (2244.2,444.5),
                          (1524.4,1549.0),
                          (4143.8,1549.0),
                          (1649.9,5557.7),
                          (2264.6,5557.7),
                          (476.8,5557.7),
                          (4618.0,5355.7),
                          (678.6,5355.7),
                          (545.3,5355.7),
                          (2474.9,5355.7),
                          (2466.2,5355.7),
                          (1606.6,5355.7),
                          (1209.6,5355.7),
                          (4625.0,5348.1),
                          (1867.4,5348.1)]


import os
from os.path import isfile,isdir
import argparse
import time

parser = argparse.ArgumentParser(prog='SAURON',
                                 description='Search and Fit peaks program')
parser.add_argument('-ra',
                    '--run-all',
                    nargs='*',
                    action='store',
                    help='If passed, sauron.py will run for the entire level\
                        scheme. This will save time because the program\
                        won\'t have to reload the csv file for every\
                        gammaray')
parser.add_argument('-sl',
                    '--single-level',
                    nargs='*',
                    action='store',
                    help='If passed SAURON will run for only the selected\
                        level')
parser.add_argument('-d',
                    '--level-directory', 
                    type=str, 
                    help='name of the subdirectory'
                        +' containing the target file')
parser.add_argument('-g',
                    '--gate', 
                    type=float, 
                    default=-1, 
                    help='Energy of the gate that you want to use for the fit')
parser.add_argument('-p', 
                    '--peak', 
                    type=float, 
                    default=-1, 
                    help='Energy of the peak that you want to fit')
parser.add_argument('--param', 
                    nargs=5, 
                    metavar=('m','q','mean','sigma','amplitude'), 
                    type=float, 
                    default=None, 
                    help='First guess for the fit parameters')
parser.add_argument('-l',
                    '--limit',
                    nargs=2,
                    metavar=('lower','upper'),
                    type=int,
                    default=(None,None),
                    help='Lower and upper limit for fit window')
parser_arguments = parser.parse_args()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.integrate import quad,IntegrationWarning


###################### Functions ##############################################
def LoadLevelScheme(_filename): 
    '''

    LoadLevelScheme(): load the excel file named '_filename' into a pandas
    dataFrame using the three columns and their names defined at the beginning
    of the code.
    This function is EXTREMELY SLOW. In a future version of the program it will
    be substitude with another function (maybe something from numpy)

    '''
    _start=time.time()
    print(f'Reading {_filename}')
    _lvlScheme = pd.read_excel(_filename,
                           sheet_name=0,
                           usecols=[start_level_colum,
                                    primary_colum,
                                    gamma_ray_energy_column,
                                    stop_level_column])
    _lvlScheme.reset_index()
    _stop=time.time()
    return _lvlScheme


def Gauss(_x,_mean,_sigma,_amplitude):
    ''' 

    Gauss(): is a gaussian function that calculates the energy
    corresponding to x (x can be array-like)

    '''
    return np.asarray(_amplitude * np.exp(-(_x-_mean)**2/(2*_sigma**2)))


def GaussPol1(_x,_mean,_sigma,_amplitude,_m,_q):
    ''' 

    GaussPol1(): is a gaussian function + a degree 1 polinomial that
    calculates the energy corresponding to x (x can be array-like)

    '''
    return np.asarray(Gauss(_x,_mean,_sigma,_amplitude) + _m*_x + _q)


def FitGauss(_hist,_par_first_guess,_limit=[0,-1]):
    ''' 

    FitGauss(): As name suggests, this function do a gaussian fit of a
    given histogram (hist).

        Inputs: - (_hist) the histogram 
                - (_par_first_guess) first guess
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
                                 p0=_par_first_guess)
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


def DrawFitResults(_hist,_level_directory,_gate_energy,_peak,_limit,_results,_show_flag=0):

    '''

    DrawFitResults():   draw the hist area inside [_limit] and the fit
                        corresponding to _results.
    
        Inputs: - (_hist) the histogram to draw
                - (_level_directory) level energy to set the title
                - (_gate_energy) gate energy to set the title
                - (_peak) peak energy to set the title
                - (_limit) lower and upper limit to draw the histogram
                  and the fit.
                - (_results) gaussian function parameters
                - (_shoe_flag) this flag is used to suppres the plt.show()
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


def SaveFitResults(_level_directory,_gate_energy,_peak,_results):
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
    _output_filename=os.path.join(_level_directory,str(_gate_energy)+'-'+str(_peak)+'.out.txt')
    _best_parameters,_cov,_I_diff,_I=_results
    with open(_output_filename,'w') as _f:
        print('Integral Diff,Integral,TRANSITION,GATE,'
               +'mean,sigma,amplitude,m,q,'
               +'err_mean,err_sigma,err_amplitude,err_m,err_q',
              file=_f)
        print(f'{_I_diff:.4f}',
              f'{_I:.4f}',
              f'{_peak:.4f}',
              f'{float(_gate_energy):.4f}',
              f'{_best_parameters[0]:.4f}',
              f'{_best_parameters[1]:.4f}',
              f'{_best_parameters[2]:.4f}',
              f'{_best_parameters[3]:.4f}',
              f'{_best_parameters[4]:.4f}',
              f'{_cov[0][0]:.4f}',
              f'{_cov[1][1]:.4f}',
              f'{_cov[2][2]:.4f}',
              f'{_cov[3][3]:.4f}',
              f'{_cov[4][4]:.4f}',
              sep=',',
              file=_f)


def SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax):
    '''

    SaveFigReuslts(): just a wrap for plt.savefig()

    '''
    _fig.savefig(os.path.join(_level_directory,
                              str(_gate_energy)+'-'+str(_peak)+'.png'),dpi=300)


def FitSinglePeak(_level_scheme,_level_directory,_gate_energy,_peak,_param=None,
                  _limit=None,_called_directly=0):
    '''

    FitSinglePeak(): wrap FitGauss() and runs it for the one selected peak.
    
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
    os.chdir(spectra_directory)
    _level_directory=os.path.join(_level_directory,'')
    _filename=str(_gate_energy)+'.dat'
    _hist = np.genfromtxt(_level_directory+_filename)
    if _param==None: _param=[_peak,2,_hist[int(_peak),1],-0.1,10]
    if _limit==None: _limit=[_peak-20,_peak+20]
    _results=FitGauss(_hist,_param,_limit)
    _fig,_ax=DrawFitResults(_hist,_level_directory,_gate_energy,_peak,_limit,_results,_show_flag=_called_directly)
    if _called_directly==1:
        if choice:=input('Do you want to save the results? [Y/n] ')!='n':
            SaveFitResults(_level_directory,_gate_energy,_peak,_results)
            SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax)
        else:
            print(f'\nFit Results\n \
                Mean: {_results[0][0]:.4f}\n \
                Sigma: {_results[0][1]:.4f}\n \
                Amplitude: {_results[0][2]:.4f}\n \
                m: {_results[0][3]:.4f}\n \
                q: {_results[0][4]:.4f}\n \
                I_diff: {_results[2]:.4f}\n \
                I: {_results[3]:.4f}')
    else:
        SaveFitResults(_level_directory,_gate_energy,_peak,_results)
        SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax)


    return _results

def FitSinglePrimaryPeak(_level_scheme):
    '''

    FitSinglePeak(): wrap FitGauss() and runs it for the one selected peak.
    
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
    os.chdir(spectra_directory) #così mi trovo dentro la cartella spectra/.
    _primary_level_scheme=_level_scheme[_level_scheme[pc_name]=='YES']
    # Here cycling over all the primary gammarays
    for _index,_primary_gammaray in _primary_level_scheme.iterrows():
        _ending_level=_primary_gammaray[stplc_name]
        for _secondary_index,_secondary_gamma_ray in _level_scheme[_level_scheme[stalc_name]==_ending_level].iterrows():
            os.chdir(os.path.join(spectra_directory,str(_secondary_gamma_ray[stplc_name])))
            _hist=np.genfromtxt(str(_secondary_gamma_ray[grec_name])+'.dat')
            print(f'{_secondary_gamma_ray[grec_name]} si trova in {os.path.join(spectra_directory,str(_secondary_gamma_ray[stplc_name]))}')


    #_primary_level_directory=os.path.join(_level_directory,'') # questa è la cartella 11131.6
    #_final_level=_level_scheme[_level_scheme[grec_name]==_peak][stplc_name]
    #print(_peak," finisce su ",final_level)
    ##_filename=str(_gate_energy)+'.dat'
    #_hist = np.genfromtxt()
    #if _param==None: _param=[_peak,2,_hist[int(_peak),1],-0.1,10]
    #if _limit==None: _limit=[_peak-20,_peak+20]
    #_results=FitGauss(_hist,_param,_limit)
    #_fig,_ax=DrawFitResults(_hist,_level_directory,_gate_energy,_peak,_limit,_results,_show_flag=_called_directly)
    #if _called_directly==1:
    #    if choice:=input('Do you want to save the results? [Y/n] ')!='n':
    #        SaveFitResults(_level_directory,_gate_energy,_peak,_results)
    #        SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax)
    #    else:
    #        print(f'\nFit Results\n \
    #            Mean: {_results[0][0]:.4f}\n \
    #            Sigma: {_results[0][1]:.4f}\n \
    #            Amplitude: {_results[0][2]:.4f}\n \
    #            m: {_results[0][3]:.4f}\n \
    #            q: {_results[0][4]:.4f}\n \
    #            I_diff: {_results[2]:.4f}\n \
    #            I: {_results[3]:.4f}')
    #else:
    #    SaveFitResults(_level_directory,_gate_energy,_peak,_results)
    #    SaveFigReuslts(_level_directory,_gate_energy,_peak,_fig,_ax)


    #return _results




def FitSingleLevel(_level_scheme,_level_directory):
    '''

    FitSingleLevel(): wrap FitGauss() and runs it for the one selected level.
    
        Inputs(): - (_level_scheme) the pandas dataFrame containing the level
                    scheme.
                  - (_level_directory) the directory to be analysed.

    '''
    os.chdir(spectra_directory)
    _energy_level=float(_level_directory)
    _subset_level_scheme_mask=_level_scheme[stalc_name]==_energy_level
    _subset_level_scheme=_level_scheme[_subset_level_scheme_mask]
    print(f'Now working on: {_level_directory}')
    for _filename in os.listdir(_level_directory):
        if _filename.endswith('.dat'):
            _gate_energy=_filename.replace('.dat','')
            _filename=os.path.join(_level_directory,_filename)
            for _index,_gammaray in _subset_level_scheme.iterrows():
                if((_gammaray[grec_name],float(_gate_energy)) in gammaray_to_be_skipped):
                    pass
                else:
                    _peak=_gammaray[grec_name]
                    _results,*_=FitSinglePeak(_level_scheme,
                                              _level_directory,
                                              _gate_energy,
                                              _peak,
                                              _called_directly=0)


def FitEntireLevelScheme(_level_scheme):
    '''

        FitEntireLevelScheme(): call FitSingleLevel() on every level directory
        present inside the spectra/ folder.
    
            Inputs(): - (_level_scheme) the pandas dataFrame containing the 
                        level scheme.

    '''
    os.chdir(spectra_directory)
    for _level_directory in os.listdir():
        if isdir(_level_directory):
            FitSingleLevel(_level_scheme,_level_directory)


###################### END of Functions ########################################


if __name__ == '__main__':

    # First step - load the level scheme ----> EXTREMELY SLOW
    # need to change read_excel() with something faster
    start_load_time=time.time()
    level_scheme=LoadLevelScheme('/home/massimiliano/Desktop/44Ca_ILL/intensities44CaCompressed.ods')
    stop_load_time=time.time()

    FitSinglePrimaryPeak(level_scheme)
    # Second step - check if the user wants to run the code for every gammaray
    # (first if()), for one single level (second if()) or for one single
    # transition (third if()).
    #if parser_arguments.run_all is not None:
    #    start_calc_time=time.time()
    #    FitEntireLevelScheme(level_scheme)
    #    stop_calc_time=time.time()
    #elif parser_arguments.single_level is not None:
    #    start_calc_time=time.time()
    #    FitSingleLevel(level_scheme,
    #                   parser_arguments.level_directory)
    #    stop_calc_time=time.time()
    #else:
    #    start_calc_time=time.time()
    #    FitSinglePeak(level_scheme,
    #                  parser_arguments.level_directory,
    #                  parser_arguments.gate,
    #                  parser_arguments.peak,
    #                  parser_arguments.param,
    #                  parser_arguments.limit,
    #                  1)
    #    stop_calc_time=time.time()

    ## Tird step - calculate execution times
    #load_time=stop_load_time-start_load_time
    #calc_time=stop_calc_time-start_calc_time
    #total_time=stop_calc_time-start_load_time

    #print('\n')
    #print(f'****************************************')
    #print(f'  ----  Loading time: {load_time//60:.0f} m {load_time-load_time//60:.0f} s')
    #print(f'  ----  Fit time: {calc_time//60:.0f} m {calc_time-calc_time//60:.0f} s')
    #print(f'  ----  Total time: {total_time//60:.0f} m {total_time-total_time//60:.0f} s')
    #print(f'****************************************')
    #print('\n')

