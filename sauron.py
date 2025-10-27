#!/usr/bin/python3

# This program is meant to check gamma-ray intensity balance on a excel file containing all the transitions of a nucleus.
# The program must be called as ./sauron.py <name_of_directory> from the Mordor directory.
# It expects a directory named spectra containing all the subdirectories with the gated energy histograms.
# The directory-tree must be structured as follows:
# 
# spectra
#
#   --> 1157.0208
#       -->energy1.dat
#       -->energy2.dat
#
#   --> level_energy_2
#       -->energy3.dat
#       -->energy4.dat
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

import os
from os.path import isdir,join
import argparse

parser = argparse.ArgumentParser(description='1 argument is required but 0 were given!')

parser.add_argument('pos_arg', type=str, help='path to the directory containing the spectra')
args = parser.parse_args()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.integrate import quad


# Step 1
# Load the excel file in a pandas dataframe using only the columns specified at the beggining of the file with 

_lvlScheme = pd.read_excel("../44Ca_ILL/intensities44CaCompressed.ods",sheet_name=0,usecols=[_start_level_colum,_gamma_ray_energy_column,_stop_level_column])
_lvlScheme.reset_index()

# Step 2
# Here two functions are defined:
#
# --> Energy(): is a gaussian function that calculates the energy corresponding to x (x can be array-like)
#
# --> FitGauss(): take and histogram as input and try to execute a fit of it using the Energy() function and returns the best parameters found and
#     the variable 'I_diff' (difference between the sum of the bin contents and the integral of the fitted funtion).
#     'I_diff' is useful to evaluate the goodness of the fit.
#     If the fit doesn't converge than the function return a set of the fitted parameters all equals to 0 (e.g. [0,0,0,0,0])
#     It also plots the histogram and the fitted function (if any!)
#

def Energy(x, m, q, mean, sigma , amplitude):
    return np.asarray(amplitude * np.exp(-(x-mean)**2/(2*sigma**2)) + m*x + q )#+ c1*np.exp(c2*(x-mean))*(1-(np.exp(c3*(x-mean)**2)/(2*sigma**2))))
    
def FitGauss(hist, q, mean, sigma, amplitude, window=6, plot_title="", fig_dir=""):

    fig, ax = plt.subplots(1,1,figsize=(7,3))
    ax.bar(hist[int(mean-window):int(mean+window),0], hist[int(mean-window):int(mean+window),1])
    
    try:
        
        parameters, _ = curve_fit(Energy, hist[int(mean-window):int(mean+window),0], hist[int(mean-window):int(mean+window),1], p0=[-0.1,q,mean,sigma,amplitude])
        appo = np.linspace(int(mean-window),int(mean+window),500)
        ax.plot(appo, Energy(appo, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]),color="darkorange")
        I_diff = int(quad(Energy,int(mean-window),int(mean+window),args=(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]))[0]-np.sum(hist[int(mean-window):int(mean+window),1]))
        I = quad(Energy,int(mean-window),int(mean+window),args=(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]))[0]
        #print("I: ", I)
        #print("parameters: ", parameters)

    except: 
       
        I_diff = int(-np.sum(hist[int(mean-window):int(mean+window),1]))
        I = 0
        parameters = [0,0,0,0,0]

#    plt.show()
    ax.set_title(plot_title)
    plt.savefig(fig_dir + plot_title.replace(" ","-") + '.png', dpi=300)
    plt.close()
    return parameters, I_diff, I


# Step 3
# Load the spectra contained in the directory passed from the command line (./sauron.py <energy_of_the_level>) 
# The name of the directory containing the gated spectra refered to one level should be equal to the energy of the level (i.e.: 1157.0208/)
# Spectra are already gated and their name should match the pattern: GammaRayEnergy.dat

if isdir(join(os.getcwd(),'spectra',args.pos_arg)):

    print('Now processing ' + args.pos_arg + ' ...')
        
    if not args.pos_arg.endswith('/'):
        spectra_directory = os.getcwd() + '/spectra/' + args.pos_arg + '/'
    else:
        spectra_directory = os.getcwd() + '/spectra/' + args.pos_arg
    
    with open(spectra_directory + args.pos_arg + '.' + 'out.txt', 'w') as f: # create the output file where fit results are stored
        
        print("Integral Diff,Integral,TRANSITION,GATE,m,q,mean,sigma,amplitude",file=f)
        
        for file in sorted(os.listdir(spectra_directory)):
        
            filename = spectra_directory+file
    
            if filename.endswith(".dat"):
                
                energyLevel = float(args.pos_arg.replace('/',''))
                h = np.genfromtxt(filename)
                subsetLevelScheme = _lvlScheme[_lvlScheme['LevelLITERATURE'] == energyLevel]
                
                for index, gammaray in subsetLevelScheme.iterrows():
                    
                    rFit, I_diff, I = FitGauss(h, h[0][1] ,gammaray['Egamma-LITERATURE'], 2, h[int(gammaray['Egamma-LITERATURE'])][1], window=6, plot_title=file.replace(".dat","") + " " + str(gammaray['Egamma-LITERATURE']), fig_dir=spectra_directory)
                    print(int(I_diff), ",", I, ",", gammaray['Egamma-LITERATURE'], ",", file.replace('.dat',''), ",", rFit[0],",",rFit[1],",",rFit[2],",",rFit[3],",",rFit[4],file=f)

else:
    pass
