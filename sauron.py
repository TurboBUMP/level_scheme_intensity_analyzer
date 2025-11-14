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

gamma_ray_energy_column = 4
grec_name='Egamma-LITERATURE'

stop_level_column = 6
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
                          (556.8,1658.8)]

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
    _start=time.time()
    print(f'Reading {_filename}')
    _lvlScheme = pd.read_excel(_filename,
                           sheet_name=0,
                           usecols=[start_level_colum,
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
                 calculates the energy corresponding to x 
                 (x can be array-like)

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
                 - zero for everything and 100000000 for (_I_diff) if 
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


def DrawFitResults(_hist,_limit,_results,_show_flag=0):

    '''
    DrawFitResults(): draw the hist area between _limit and the fit corresponding
    to _results
    '''

    _lower,_upper=_limit
    _lower=int(_lower)
    _upper=int(_upper)
    _parameters,*_=_results
    _fig,_ax=plt.subplots(1,1,figsize=(7,3))
    _energy_axis=np.linspace(_lower,_upper,500)
    _ax.bar(_hist[_lower:_upper,0],_hist[_lower:_upper,1])
    _ax.plot(_energy_axis,GaussPol1(_energy_axis,*_parameters),color='darkorange')
    if _show_flag:
        plt.show()
    plt.close()

    return _fig,_ax


def SaveFitResults(_level_directory,_gate_energy,_peak,_results):
    os.chdir(spectra_directory)
    _output_filename=os.path.join(_level_directory,str(_gate_energy)+'-'+str(_peak)+'.out.txt')
    _best_parameters,_cov,_I_diff,_I=_results
    with open(_output_filename,'w') as _f:
        print('Integral Diff,Integral,TRANSITION,GATE,\
               mean,sigma,amplitude,m,q,\
               err_mean,err_sigma,err_amplitude,err_m,err_q',
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
    _fig.savefig(os.path.join(_level_directory,
                              str(_gate_energy)+'-'+str(_peak)+'.png'),dpi=300)


def FitSinglePeak(_level_scheme,_level_directory,_gate_energy,_peak,_param=None,
                  _limit=None,_called_directly=0):
    ''' 
    FitSinglePeak(): wrap FitGauss() and runs it for the one selected peak.
    '''
    os.chdir(spectra_directory)
    _level_directory=os.path.join(_level_directory,'')
    _filename=str(_gate_energy)+'.dat'
    _hist = np.genfromtxt(_level_directory+_filename)
    if _param==None: _param=[_peak,2,_hist[int(_peak),1],-0.1,10]
    if _limit==None: _limit=[_peak-20,_peak+20]
    _results=FitGauss(_hist,_param,_limit)
    _fig,_ax=DrawFitResults(_hist,_limit,_results,_show_flag=_called_directly)
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


def FitSingleLevel(_level_scheme,_level_directory):
    '''
    FitSingleLevel(): wrap FitGauss() and runs it for the one selected level.
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
    os.chdir(spectra_directory)
    for _level_directory in os.listdir():
        if isdir(_level_directory):
            FitSingleLevel(_level_scheme,_level_directory)


###################### END of Functions ########################################


if __name__ == '__main__':

    start_load_time=time.time()
    level_scheme=LoadLevelScheme('../44Ca_ILL/intensities44CaCompressed.ods')
    stop_load_time=time.time()

    if parser_arguments.run_all is not None:
        start_calc_time=time.time()
        FitEntireLevelScheme(level_scheme)
        stop_calc_time=time.time()
    elif parser_arguments.single_level is not None:
        start_calc_time=time.time()
        FitSingleLevel(level_scheme,
                       parser_arguments.level_directory)
        stop_calc_time=time.time()
    else:
        start_calc_time=time.time()
        FitSinglePeak(level_scheme,
                      parser_arguments.level_directory,
                      parser_arguments.gate,
                      parser_arguments.peak,
                      parser_arguments.param,
                      parser_arguments.limit,
                      1)
        stop_calc_time=time.time()

    load_time=stop_load_time-start_load_time
    calc_time=stop_calc_time-start_calc_time
    total_time=stop_load_time-start_load_time

    print('\n')
    print(f'****************************************')
    print(f'  ----  Loading time: {load_time//60:.0f} m {load_time-load_time//60:.0f} s')
    print(f'  ----  Fit time: {calc_time//60:.0f} m {calc_time-calc_time//60:.0f} s')
    print(f'  ----  Total time: {total_time//60:.0f} m {total_time-total_time//60:.0f} s')
    print(f'****************************************')
    print('\n')

