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
start_level_colum = 0
gamma_ray_energy_column = 4
stop_level_column = 6

lvl_scheme = pd.read_excel(
        "/home/massimiliano/Desktop/44Ca_ILL/intensities44CaCompressed.ods",
        sheet_name=0,
        usecols=[start_level_colum,gamma_ray_energy_column,stop_level_column])
lvl_scheme.reset_index()


# Load the file containing all the FIT output for every gammaray
intensity_file = pd.read_csv("/home/massimiliano/Desktop/Mordor/output.txt")
intensity_file.reset_index()


# Parameters definition for the efficiency function
fit_parameters = [-0.423449,
                  -0.832414,
                  -0.714755,
                  +0.274499,
                  +0.034013,
                  -0.0159099]
fit_parameters_error = [0.0581693,
                        0.0520197,
                        0.0258968,
                        0.0107855,
                        0.00310721,
                        0.000739547]


########### FUNCTION DEFINITION #############

# Efficiency function (see MecFarland et al., "Behavior of Several Germanium Detector Full Energy Peak"
# as reference for this function)
# The parameters were fitted with the efficiencyFIT.C ROOT macro.
def efficiency(energy,args=[]):
    efficiency = np.exp(args[0]
            +args[1]*np.log(energy/200)
            +args[2]*np.log(energy/200)**2
            +args[3]*np.log(energy/200)**3
            +args[4]*np.log(energy/200)**4
            +args[5]*np.log(energy/200)**5)
    return efficiency

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

    gate_list = np.asarray(intensity_file[intensity_file['TRANSITION'].isin([gammaray_energy])]['GATE'])
    gammaray_intensity_list = np.asarray(intensity_file[intensity_file['TRANSITION'].isin([gammaray_energy])]['Integral'])
    gate_efficiency_list = np.asarray(efficiency(gate_list,args=fit_parameters))
    gammaray_efficiency = efficiency(gammaray_energy,args=fit_parameters)
    weighted_efficiency_list = gammaray_intensity_list * gate_efficiency_list

    return weighted_efficiency_list.sum() * gammaray_efficiency

## This function take the energy level as argument and return two np.array: 
## 1- array containing the outgoing gammaray list
## 2- array containing the outgoing gammaray intensity list
#def level_outgoing_intensity_calc(energy_level):
#
#    outgoing_gammaray_list = find_outgoing(energy_level)
#    outgoing_gammaray_intensity_list = np.asarray([gammaray_intensity_calc(gammaray) for gammaray in outgoing_gammaray_list])
#
#    return outgoing_gammaray_list, outgoing_gammaray_intensity_list
#
## This function take the energy level as argument and return two np.array: 
## 1- array containing the incoming gammaray list
## 2- array containing the incoming gammaray intensity list
#def level_incoming_intensity_calc(energy_level):
#
#    incoming_gammaray_list = find_incoming(energy_level)
#    incoming_gammaray_intensity_list = np.asarray([gammaray_intensity_calc(gammaray) for gammaray in incoming_gammaray_list])
#
#    return incoming_gammaray_list, incoming_gammaray_intensity_list

#############################################

#-------------------------------------------#

################## MAIN #####################

if __name__ == '__main__':

    with open('intensity_output.txt','w') as f:

        for gammaray in lvl_scheme['Egamma-LITERATURE']:

            intensity = gammaray_intensity_calc(gammaray)
            print(gammaray, ' ', intensity, file=f)

