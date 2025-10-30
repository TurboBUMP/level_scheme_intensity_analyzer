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
#gammaray_to_be_skipped = [(263.53,887.5)]
gammaray_to_be_skipped = []

import os
from os.path import isdir,join
import argparse

parser = argparse.ArgumentParser(prog='SAURON',
                                 description='Search and Fit peaks program')
parser.add_argument('path', 
                    type=str, 
                    help='path to the directory containing the spectra')
parser.add_argument('-g',
                    '--gate', 
                    type=float, 
                    default=-1, 
                    help='energy of the gate that you want to use for the fit')
parser.add_argument('-p', 
                    '--peak', 
                    type=float, 
                    default=-1, 
                    help='energy of the peak that you want to fit')
parser.add_argument('--param', 
                    nargs=5, 
                    metavar=('m','q','mean','sigma','amplitude'), 
                    type=float, 
                    default=None, 
                    help='first guess for the fit parameters')
args = parser.parse_args()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.integrate import quad


# Step 1
# Load the excel file in a pandas dataframe using only the columns specified at the beggining of the file with 

_lvlScheme = pd.read_excel("../44Ca_ILL/intensities44CaCompressed.ods",
                           sheet_name=0,
                           usecols=[_start_level_colum,_gamma_ray_energy_column,_stop_level_column])
_lvlScheme.reset_index()

# Step 2
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

def Gauss(x, mean, sigma, amplitude):
    return np.asarray(amplitude * np.exp(-(x-mean)**2/(2*sigma**2)))

def GaussPol1(x, m, q, mean, sigma , amplitude):
    return np.asarray(amplitude * np.exp(-(x-mean)**2/(2*sigma**2)) + m*x + q )#+ c1*np.exp(c2*(x-mean))*(1-(np.exp(c3*(x-mean)**2)/(2*sigma**2))))
    
def FitGauss(hist, q, mean, sigma, amplitude, window=6, plot_title="", fig_dir="", par=[], savefig_flag=False):
    if(par==None):
        par=[-0.1,q,mean,sigma,amplitude]

    fig, ax = plt.subplots(1,1,figsize=(7,3))
    ax.bar(hist[int(mean-window):int(mean+window),0], hist[int(mean-window):int(mean+window),1])
    
    try:
        
        parameters, _ = curve_fit(GaussPol1, 
                                  hist[int(mean-window):int(mean+window),0], 
                                  hist[int(mean-window):int(mean+window),1], 
                                  p0=par)
        appo = np.linspace(int(mean-window),int(mean+window),500)
        ax.plot(appo, 
                GaussPol1(appo, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]),
                color="darkorange")
        I_diff = int(quad(GaussPol1,int(mean-window),int(mean+window),args=(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]))[0]-np.sum(hist[int(mean-window):int(mean+window),1]))
        I = quad(Gauss,
                 int(mean-window),int(mean+window),
                 args=(parameters[2], parameters[3], parameters[4]))[0]

    except: 
       
        I_diff = int(-np.sum(hist[int(mean-window):int(mean+window),1]))
        I = 0
        parameters = [0,0,0,0,0]

    
    ax.set_title(plot_title)

    if (savefig_flag==True):
        plt.savefig(fig_dir + plot_title.replace(" ","-") + '.png', dpi=300)
    if (savefig_flag==False):
        if (input('Do you want to save the figure? (the fit params will not be automatically stored in the output.txt file\n')):
            plt.savefig(fig_dir + plot_title.replace(" ","-") + 'png', dpi=300)
        else:
            pass
    
    if (args.peak != -1):
        plt.show()

    plt.close()
    
    return parameters, I_diff, I


# Step 3
# Load the spectra contained in the directory passed from the command line (./sauron.py <energy_of_the_level>) 
# The name of the directory containing the gated spectra refered to one level should be equal to the energy of the level (i.e.: 1157.0208/)
# Spectra are already gated and their name should match the pattern: GammaRayEnergy.dat


if __name__ == '__main__':

    if (args.peak != -1):
        
        print('Fitting only selected peak: ', args.peak)

        if not args.path.endswith('/'):
            spectra_directory = os.getcwd() + '/spectra/' + args.path + '/'
        else:
            spectra_directory = os.getcwd() + '/spectra/' + args.path
           
        file = str(args.gate) + '.dat'
        filename = spectra_directory + file 

        energyLevel = float(args.path.replace('/',''))
        h = np.genfromtxt(filename)
        subsetLevelScheme = _lvlScheme[_lvlScheme['LevelLITERATURE'] == energyLevel]
        gammaray = args.peak

        rFit, I_diff, I = FitGauss(h, 
                                   h[0][1] ,
                                   gammaray, 
                                   2, 
                                   h[int(gammaray)][1], 
                                   window=6, 
                                   plot_title=file.replace(".dat","") + " " + str(gammaray), 
                                   fig_dir=spectra_directory, 
                                   par=args.param)
        
        print("Integral Diff,Integral,TRANSITION,GATE,m,q,mean,sigma,amplitude",file=f)
        print(int(I_diff), ",",
              I, ",",
              gammaray, ",",
              file.replace('.dat',''), ",",
              rFit[0],",",
              rFit[1],",",
              rFit[2],",",
              rFit[3],",",
              rFit[4])
        
    else:

        if isdir(join(os.getcwd(),'spectra',args.path)):
        
            print('Now processing ' + args.path + ' ...')
             
            if not args.path.endswith('/'):
                spectra_directory = os.getcwd() + '/spectra/' + args.path + '/'
            else:
                spectra_directory = os.getcwd() + '/spectra/' + args.path
            
            with open(spectra_directory + args.path + '.' + 'out.txt', 'w') as f: # create the output file where fit results are stored
                
                print("Integral Diff,Integral,TRANSITION,GATE,m,q,mean,sigma,amplitude",file=f)
                
                for file in sorted(os.listdir(spectra_directory)):
                
                    filename = spectra_directory+file
         
                    if filename.endswith(".dat"):
                        
                        energyLevel = float(args.path.replace('/',''))
                        h = np.genfromtxt(filename)
                        subsetLevelScheme = _lvlScheme[_lvlScheme['LevelLITERATURE'] == energyLevel]
                        
                        for index, gammaray in subsetLevelScheme.iterrows():
        
                            if((gammaray['Egamma-LITERATURE'],float(file.replace('.dat',''))) in gammaray_to_be_skipped):

                                print(1000000, ",", 
                                      0, ",", 
                                      gammaray['Egamma-LITERATURE'], ",", 
                                      file.replace('.dat',''), ",", 
                                      0,",",
                                      0,",",
                                      0,",",
                                      0,",",
                                      0,
                                      file=f)

                            else:
                                rFit, I_diff, I = FitGauss(h, 
                                                           h[0][1], 
                                                           gammaray['Egamma-LITERATURE'],
                                                           2, 
                                                           h[int(gammaray['Egamma-LITERATURE'])][1], 
                                                           window=6, 
                                                           plot_title=file.replace(".dat","") + " " + str(gammaray['Egamma-LITERATURE']), 
                                                           fig_dir=spectra_directory, 
                                                           savefig=True)
                                print(int(I_diff),
                                      ",",
                                      I, 
                                      ",",
                                      gammaray['Egamma-LITERATURE'], ",",
                                      file.replace('.dat',''), ",",
                                      rFit[0],",",
                                      rFit[1],",",
                                      rFit[2],",",
                                      rFit[3],",",
                                      rFit[4],
                                      file=f)
        
        else:
            pass
