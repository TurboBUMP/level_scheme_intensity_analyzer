#!/usr/bin/python3

import os
import argparse

parser = argparse.ArgumentParser(description='Questo è il parser! Usalo con cura')

parser.add_argument('pos_arg', type=str, help='path to the directory containing the spectra')
args = parser.parse_args()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.integrate import quad


# # Step 1
# ## Load the excel file in a pandas dataframe

lvlScheme = pd.read_excel("../44Ca_ILL/intensities44CaCompressed.ods",sheet_name=0,usecols=[0,4,6])
lvlScheme.reset_index()

# # Step 2
# ## Define some useful functions

def Energy(x, m, q, mean, sigma , amplitude):
    return np.asarray(amplitude * np.exp(-(x-mean)**2/(2*sigma**2)) + m*x + q )#+ c1*np.exp(c2*(x-mean))*(1-(np.exp(c3*(x-mean)**2)/(2*sigma**2))))
    
def FitGauss(hist, q, mean, sigma, amplitude, window=6, plot_title="", fig_dir=""):

    fig, ax = plt.subplots(1,1,figsize=(7,3))
    ax.bar(hist[int(mean-window):int(mean+window),0], hist[int(mean-window):int(mean+window),1])
    
    try:
        
        parameters, _ = curve_fit(Energy, hist[int(mean-window):int(mean+window),0], hist[int(mean-window):int(mean+window),1], p0=[-0.1,q,mean,sigma,amplitude])
        appo = np.linspace(int(mean-window),int(mean+window),500)
        ax.plot(appo, Energy(appo, parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]),color="darkorange")
        I = int(quad(Energy,int(mean-window),int(mean+window),args=(parameters[0], parameters[1], parameters[2], parameters[3], parameters[4]))[0]-np.sum(hist[int(mean-window):int(mean+window),1]))
        #print("I: ", I)
        #print("parameters: ", parameters)

    except: 
       
        #print(1, q, "mean: ", mean, "sigma: ", sigma, "amp: ", amplitude)
        #print("Error - curve_fit failed")
        #print("I: ", -np.sum(hist[int(mean-window):int(mean+window),1]))
        I = int(-np.sum(hist[int(mean-window):int(mean+window),1]))
        #print("I: ", I)
        parameters = [0,0,0,0,0]

#    plt.show()
    ax.set_title(plot_title)
    plt.savefig(fig_dir + plot_title.replace(" ","-") + '.png', dpi=300)
    plt.close()
    return parameters, I


# # Step 3
# ## Load the spectra and do the analysis 
# ### Spectra are already gated and their name should match the pattern: PopulatingLevelEnergy-GammaRayEnergy.dat

spectra_directory = os.getcwd() + '/spectra/' + args.pos_arg + '/'

with open(spectra_directory + args.pos_arg + '.' + 'out.txt', 'w') as f:
    
    print("Integral Diff, TRANSITION,GATE, m, q, mean, sigma, amplitude",file=f)
    
    for file in sorted(os.listdir(spectra_directory)):
    
        filename = spectra_directory+file

        if filename.endswith(".dat"):
    
            energyLevel = float(file.split("#")[0])
            h = np.genfromtxt(filename)
            subsetLevelScheme = lvlScheme[lvlScheme['LevelLITERATURE'] == energyLevel]
            
            for index, gammaray in subsetLevelScheme.iterrows():
                
                rFit, I = FitGauss(h, h[0][1] ,gammaray['Egamma-LITERATURE'], 2, h[int(gammaray['Egamma-LITERATURE'])][1], window=6, plot_title=file.replace(".dat","") + " " + str(gammaray['Egamma-LITERATURE']), fig_dir=spectra_directory)
                print(int(I), ",", gammaray['Egamma-LITERATURE'], ",", file.split("#")[1].split(".")[0], ",", rFit[0],",",rFit[1],",",rFit[2],",",rFit[3],",",rFit[4],file=f)
