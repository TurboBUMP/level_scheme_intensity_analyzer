#!/usr/bin/python3

# This program is meant to check gamma-ray intensity balance on a excel file containing all the transitions of a nucleus.
# The program must be called as ./sauron.py <name_of_directory> from the Mordor directory.
# Example: ./sauron.py 1157.0208
#
# It expects a directory named spectra containing all the subdirectories with the gated energy histograms.
# The directory-tree must be structured as follows:
# 
# spectra
#
#   --> level_energy_1
#       gate_energy_1.dat
#       gate_energy_2.dat
#
#   --> level_energy_2
#       gate_energy_3.dat
#       gate_energy_4.dat
#
# The excel file must contain three columns stating for each transition: [start level, gamma ray energy, stop level]
# The first line must contain the name of each column to let Pandas be able to initialise the dataFrame properly. 
# 
# Example: 
#       _start_level_colum = 1 
#       _gamma_ray_energy_column = 2
#       _stop_level_column = 3
#
#

_start_level_colum = 0 
_gamma_ray_energy_column = 4
_stop_level_column = 6 

# 'gammaray_to_be_skipped' is a list of pairs that stores all the pairs of gate-and-spectra that (for some reasons)
# need to be skipped.
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

parser = argparse.ArgumentParser(prog='SAURON',
                                 description='Search and Fit peaks program')
parser.add_argument('--run-all',
                    type=None,
                    default=None,
                    help='If passed, sauron.py will run for the entire level scheme.'
                        +'This will save time because the program won\'t have to reload'
                        +'the csv file for every gammaray')
parser.add_argument('path', 
                    type=str, 
                    help='[REQUIRED] path to the directory containing the spectra')
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
from scipy.integrate import quad

# Here two functions are defined:
#
# --> GaussPol1(): is a gaussian function that calculates the energy corresponding to x (x can be array-like)
#
# --> FitGauss(): take and histogram as input and try to execute a fit of it using the GaussPol1() function and returns the best parameters found and
#     the variable 'I_diff' (difference between the sum of the bin contents and the integral of the fitted funtion).
#     'I_diff' is useful to evaluate the goodness of the fit.
#     If the fit doesn't converge than the function return a set of the fitted parameters all equals to 0 (e.g. [0,0,0,0,0])
#     It also plots the histogram and the fitted function (if any!)
#


def Gauss(x,mean,sigma,amplitude):
    return np.asarray(amplitude * np.exp(-(x-mean)**2/(2*sigma**2)))


def GaussPol1(x,m,q,mean,sigma,amplitude):
    return np.asarray(amplitude * np.exp(-(x-mean)**2/(2*sigma**2)) + m*x + q )#+ c1*np.exp(c2*(x-mean))*(1-(np.exp(c3*(x-mean)**2)/(2*sigma**2))))

 
def FitGauss(hist,q,mean,amplitude,limit,par):
    lower,upper=limit
    lower=int(lower)
    upper=int(upper)
    try:
        parameters,cov=curve_fit(GaussPol1,
                                 hist[lower:upper,0],
                                 hist[lower:upper,1],
                                 p0=par)
        I=np.sum(hist[lower,upper,1])
        I_diff=int(quad(GaussPol1,lower,upper,*parameters)[0]-I)
    except:
        I=0
        I_diff=1000000000
        parameters=[0,0,0,0,0]
        cov=[[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],]
        
    return parameters,cov,I_diff,I


def FitSinglePeak(path,gate,peak,param,limit):
    # The following line is just to make sure that the path ends with /
    # ---> os.path.join() make it automatically
    spectra_directory=os.path.join(os.getcwd()+parser_arguments.path,'')


if __name__ == '__main__':

    print(parser_arguments.limit)
