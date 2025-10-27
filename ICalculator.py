#!/usr/bin/python3

import pandas as pd
import numpy as np
import os 
from os.path import join,isdir,isfile

start_level_colum = 0
gamma_ray_energy_column = 4
stop_level_column = 6

lvl_scheme = pd.read_excel(
        "/home/massimiliano/Desktop/44Ca_ILL/intensities44CaCompressed.ods",
        sheet_name=0,
        usecols=[start_level_colum,gamma_ray_energy_column,stop_level_column])
lvl_scheme.reset_index()

intensity_file = pd.read_csv("/home/massimiliano/Desktop/Mordor/output.txt")
intensity_file.reset_index()

def find_outgoing(energy_level):
    return np.asarray(lvl_scheme[lvl_scheme['LevelLITERATURE'].isin([energy_level])]['Egamma-LITERATURE'])

def find_incoming(energy_level):
    return np.asarray(lvl_scheme[lvl_scheme['Level_final'].isin([energy_level])]['Egamma-LITERATURE'])

def gammaray_intensity_calc(gammaray_energy):
    gammaray_intensity = np.asarray(intensity_file[intensity_file['TRANSITION'].isin([gammaray_energy])]['Integral'])
    return gammaray_list.sum()

print(intensity_file.keys())
#print(gammaray_intensity_calc(1157.0040))

#print('OUTGOING:\r', find_outgoing(4011.4))
#print('INCOMING:\r', find_incoming(4011.4))


