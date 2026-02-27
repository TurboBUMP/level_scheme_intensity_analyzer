#!/bin/python3.12

# This python script counts how many .dat file are present in the spectra sub-directories and if, for 
# any gamma-ray transition in the excel file, there is the corresponding .dat somewhere in one of 
# the sub-directories
# It is useful only to check if every necessary gated spectra was produced and correctly stored in the
# corresponding directory
# 

import os
from os.path import isdir, join
import pandas as pd

_lvl = pd.read_excel("../../44Ca_ILL/intensities44CaCompressed.ods", sheet_name=0, usecols=[0,4,6])
_lvl.reset_index()

dirs = [dir for dir in os.listdir() if isdir(dir)]

for energy in _lvl['Egamma-LITERATURE']:
    energyIsPresent = False
    for dir in dirs:
        for file in os.listdir(join(os.getcwd(),dir)):
            if file.endswith('.dat'):
                if (float(energy) == float(file.replace('.dat',''))):
                    energyIsPresent=True
                else:
                    pass

    if energyIsPresent==False:
        print(energy)
