#!/usr/bin/env python3

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
#       start_level_column=1 
#       primary_column=4
#       gamma_ray_energy_column=5
#       stop_level_column=7
#
# Here after you can specify you own columns number and the name of each column
#
################################################################################
################################ LIBRARY #######################################

import sys
import warnings
import time

import argparse

from functions import LoadLevelScheme,LoadToBeSkipped
from functions import FitSinglePeak
from functions import FitSingleLevel
from functions import FitSinglePrimaryPeak
from functions import FitSpecial
from functions import FitBindingLevel
from functions import FitEntireLevelScheme

################################ END LIBRARY ###################################
################################################################################

################################################################################
################################ PARSER ########################################

parser=argparse.ArgumentParser(prog='SAURON',
                                 description='Search and Fit peaks program')
parser.add_argument('-ra',
                    '--run-all',
                    nargs='*',
                    action='store',
                    help='If passed, sauron.py will run for the entire level\
                        scheme. This will save time because the program\
                        won\'t have to reload the csv file for every\
                        gammaray')
parser.add_argument('--binding',
                    nargs='*',
                    action='store',
                    help='Use this option to fit all the primary peaks')
parser.add_argument('--special',
                    nargs='*',
                    action='store',
                    help='Use this option to fit special peaks defined inside'
                    +'the single-spectra file.')
parser.add_argument('-sl',
                    '--single-level',
                    nargs='*',
                    action='store',
                    help='If passed SAURON will run for only the selected\
                        level')
parser.add_argument('--primary',
                    nargs='*',
                    action='store',
                    help='Use this argument if the gammaray you want to fit is'
                        +'a primary')
parser.add_argument('-gd',
                    '--gatedir',
                    default=None,
                    type=str,
                    help='If the single peak to fit is a primary, us --gatedir '
                        +'to specify in which directory is the gated '
                        +'spectra to use.')
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
parser.add_argument('--dont-ask',
                    nargs='*',
                    action='store',
                    default=None,
                    help='Use this argument to tell the program you don\'t want'
                    +' to be asked to save the results.'
                    +'This is useful when calling calling long sequences of'
                    +'sauron command (e.g. from a script)')
parser_arguments=parser.parse_args()

################################ END PARSER ####################################
################################################################################


if __name__ == '__main__':

    # First step - load the level scheme ----> EXTREMELY SLOW
    start_load_time=time.time()
    level_scheme=LoadLevelScheme('intensities44Ca.ods')
    gammaray_to_be_skipped = LoadToBeSkipped('to_be_skipped.txt')
    stop_load_time=time.time()

    # Second step - check if the user wants to run the code for every gammaray
    # (first if()), for one single level (second if()), for one single primary
    # transition (third if()) or for one single secondary transition.
    if parser_arguments.run_all is not None:
        start_calc_time=time.time()
        warnings.filterwarnings('ignore')
        FitEntireLevelScheme(level_scheme,gammaray_to_be_skipped)
        stop_calc_time=time.time()
    elif parser_arguments.special is not None:
        start_calc_time=time.time()
        FitSpecial(level_scheme)
        stop_calc_time=time.time()
    elif parser_arguments.single_level is not None:
        start_calc_time=time.time()
        FitSingleLevel(level_scheme,gammaray_to_be_skipped,
                       parser_arguments.level_directory)
        stop_calc_time=time.time()
    elif parser_arguments.primary is not None:
        start_calc_time=time.time()
        if parser_arguments.dont_ask is not None:
            called_directly=0
        else:
            called_directly=1
            
        FitSinglePrimaryPeak(level_scheme,
                             parser_arguments.level_directory,
                             parser_arguments.peak,
                             parser_arguments.gate,
                             parser_arguments.gatedir,
                             parser_arguments.param,
                             parser_arguments.limit,
                             called_directly)
        stop_calc_time=time.time()
    elif parser_arguments.binding is not None:
        start_calc_time=time.time()
        FitBindingLevel(level_scheme,gammaray_to_be_skipped)
        stop_calc_time=time.time()
    else:
        start_calc_time=time.time()
        if parser_arguments.dont_ask is not None:
            called_directly=0
        else:
            called_directly=1

        FitSinglePeak(level_scheme,
                      parser_arguments.level_directory,
                      parser_arguments.gate,
                      parser_arguments.peak,
                      parser_arguments.param,
                      parser_arguments.limit,
                      called_directly)
        stop_calc_time=time.time()

    # Tird step - calculate execution times
    load_time=stop_load_time-start_load_time
    calc_time=stop_calc_time-start_calc_time
    total_time=stop_calc_time-start_load_time

    print('\n')
    print(f'****************************************')
    print(f'  ----  Loading time: {load_time//60:.0f} m {load_time-load_time//60:.0f} s')
    print(f'  ----  Fit time: {calc_time//60:.0f} m {calc_time-calc_time//60:.0f} s')
    print(f'  ----  Total time: {total_time//60:.0f} m {total_time-total_time//60:.0f} s')
    print(f'****************************************')
    print('\n')
