#!/usr/bin/python3

import pandas as pd
import numpy as np
import os 
from os.path import join,isdir,isfile

# Load the spectra excel file in a pandas dataFrame called lvl_scheme
# Use start_level_colum, gamma_ray_energy_column and stop_level_column to define the columns used in the excel file: 
# --> start_level_column: column containing the energy of the level depopulated by the gammaray
# --> gamma_ray_energy_column: column containing the energy of the gammaray
# --> stop_level_column: column containing the energy of the level populated by the gammaray
#

start_level_colum = 0
gamma_ray_energy_column = 4
stop_level_column = 6

lvl_scheme = pd.read_excel(
        "/home/massimiliano/Desktop/44Ca_ILL/intensities44CaCompressed.ods",
        sheet_name=0,
        usecols=[start_level_colum,gamma_ray_energy_column,stop_level_column])
lvl_scheme.reset_index()

# Load the file containing all the FIT output for every gammaray
#

intensity_file = pd.read_csv("/home/massimiliano/Desktop/Mordor/output.txt")
intensity_file.reset_index()

########### FUNCTION DEFINITION #############

# This function take the level energy as argument and return an np.array
# containing the energy of all the gammarays depopulating the level
def find_outgoing(energy_level):
    return np.asarray(lvl_scheme[lvl_scheme['LevelLITERATURE'].isin([energy_level])]['Egamma-LITERATURE'])

# This function take the level energy as argument and return an np.array
# containing the energy of all the gammarays populating the level
def find_incoming(energy_level):
    return np.asarray(lvl_scheme[lvl_scheme['Level_final'].isin([energy_level])]['Egamma-LITERATURE'])

# This function take the gammaray energy as argument and ... [TO BE COMPLETED]
def gammaray_intensity_calc(gammaray_energy):
    gammaray_intensity = np.asarray(intensity_file[intensity_file['TRANSITION'].isin([gammaray_energy])]['Integral'])
    return gammaray_intensity.sum()

# This function take the energy level as argument and return two np.array: 
# 1- array containing the outgoing gammaray list
# 2- array containing the outgoing gammaray intensity list
def level_outgoing_intensity_calc(energy_level):
    outgoing_gammaray_list = find_outgoing(energy_level)
    outgoing_gammaray_intensity_list = np.asarray([gammaray_intensity_calc(gammaray) for gammaray in outgoing_gammaray_list])
    return outgoing_gammaray_list, outgoing_gammaray_intensity_list

# This function take the energy level as argument and return two np.array: 
# 1- array containing the incoming gammaray list
# 2- array containing the incoming gammaray intensity list
def level_incoming_intensity_calc(energy_level):
    incoming_gammaray_list = find_incoming(energy_level)
    incoming_gammaray_intensity_list = np.asarray([gammaray_intensity_calc(gammaray) for gammaray in incoming_gammaray_list])
    return incoming_gammaray_list, incoming_gammaray_intensity_list

#############################################

#-------------------------------------------#

################## MAIN #####################

if __name__ == '__main__':
    print("Hello World!")

    I_out = level_outgoing_intensity_calc(1883.516)[1].sum()
    print(I_out)
    I_in = level_incoming_intensity_calc(1883.516)[1].sum()
    print(I_in)
