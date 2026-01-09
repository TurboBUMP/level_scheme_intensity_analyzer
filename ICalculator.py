#!/usr/bin/python3

import pandas as pd
import argparse
import numpy as np
import os 
from os.path import join,isdir,isfile

np.seterr(divide='ignore', invalid='ignore')

# Load the spectra excel file in a pandas dataFrame called lvl_scheme
# Use start_level_colum, gamma_ray_energy_column and stop_level_column to define the columns used in the excel file: 
# --> start_level_column: column containing the energy of the level depopulated by the gammaray
# --> gamma_ray_energy_column: column containing the energy of the gammaray
# --> stop_level_column: column containing the energy of the level populated by the gammaray
start_level_colum = 0
gamma_ray_energy_column = 5
stop_level_column = 7

stalc_name='LevelLITERATURE'
grec_name='Egamma-LITERATURE'
stplc_name='Level_final'

def load_scheme():
    lvl_scheme = pd.read_excel(
            "/home/massimiliano/Desktop/44Ca_ILL/intensities44CaCompressed.ods",
            sheet_name=0,
            usecols=[start_level_colum,gamma_ray_energy_column,stop_level_column])
    lvl_scheme.reset_index()
    return lvl_scheme

lvl_scheme = load_scheme()


# Load the file containing all the FIT output for every gammaray
def load_intensity():
    intensity_file = pd.read_csv("/home/massimiliano/Desktop/Mordor/output.txt")
    intensity_file.reset_index()
    return intensity_file

intensity_file = load_intensity()

parser = argparse.ArgumentParser(prog='SAURON',
                                 description='Search and Fit peaks program')
parser.add_argument('-a',
                    '--analysis',
                    nargs='*',
                    action='store',
                    default=None,
                    help='If passed, program run in analysis mode.\
                        the energy of the level to be analysed will be asked')

parser_arguments = parser.parse_args()

# Class to print colored text on terminal
class bcolors:
    HEADER='\033[95m'
    OKBLUE='\033[94m'
    OKCYAN='\033[96m'
    OKGREEN='\033[92m'
    WARNING='\033[93m'
    FAIL='\033[91m'
    ENDC='\033[0m'
    BOLD='\033[1m'
    UNDERLINE='\033[4m'
    WHITE='\033[37m'

class cursor:
    LINE_CLEAR='\x1b[2K'
    LINE_UP='\033[1A'


def efficiency(energy):
    mask = np.isin(eff_vector[:,0],int(energy))
    return eff_vector[mask][0,1]

def efficiency_error(energy):
    mask = np.isin(eff_vector[:,0],int(energy))
    return eff_vector[mask][0,2]

# This function take the level energy as argument and return an np.array
# containing the energy of all the gammarays depopulating the level
def find_outgoing(energy_level):
    return np.asarray(lvl_scheme[lvl_scheme['LevelLITERATURE']==energy_level]['Egamma-LITERATURE'])

# This function take the level energy as argument and return an np.array
# containing the energy of all the gammarays populating the level
def find_incoming(energy_level):
    return np.asarray(lvl_scheme[lvl_scheme['Level_final']==energy_level]['Egamma-LITERATURE'])

# This function take the gammaray energy as argument and ... [TO BE COMPLETED]
def gammaray_intensity_calc(gammaray_energy,analyser=0):

    gate_list = np.asarray(intensity_file[intensity_file['TRANSITION']==gammaray_energy]['GATE'])
    amplitude_list = np.asarray(intensity_file[intensity_file['TRANSITION']==gammaray_energy]['amplitude'])
    sigma_list = np.asarray(intensity_file[intensity_file['TRANSITION']==gammaray_energy]['sigma'])
    gammaray_intensity_list = np.asarray(amplitude_list*np.abs(sigma_list)*np.sqrt(np.pi*2)) # I = A*sigma*sqrt(2Pi)
    gate_efficiency_list = np.asarray([efficiency(gate) for gate in gate_list])
    gammaray_efficiency = efficiency(gammaray_energy)
    gammaray_intensity_list = gammaray_intensity_list / gate_efficiency_list / gammaray_efficiency # Re-normalizing the intensity for the efficiencies of gate and gammaray

    # Ok, ora calcolo l'errore sull'intensità tenendo conto degli errori sulle ampiezze e sulle sigma dei picchi fittati
    error_amplitude_list = np.asarray(intensity_file[intensity_file['TRANSITION']==gammaray_energy]['err_amplitude'])
    error_sigma_list = np.asarray(intensity_file[intensity_file['TRANSITION']==gammaray_energy]['err_sigma'])
    error_gate_efficiency_list = np.asarray([efficiency_error(gate) for gate in gate_list])
    error_gammaray_efficiency = efficiency_error(gammaray_energy)

    error_gate_intensity_list = np.sqrt(2*np.pi)*np.sqrt((error_amplitude_list*sigma_list/(gate_efficiency_list*gammaray_efficiency))**2
                                                         +(error_sigma_list*amplitude_list/(gate_efficiency_list*gammaray_efficiency))**2
                                                         +(amplitude_list*sigma_list*error_gate_efficiency_list/(gate_efficiency_list**2*gammaray_efficiency))**2
                                                         +(amplitude_list*sigma_list*error_gammaray_efficiency/(gate_efficiency_list*gammaray_efficiency**2))**2)
    error_gammaray_intensity = np.sqrt(np.sum(error_gate_intensity_list**2))
    if analyser!=0:
        print('')
        print('************************************** IN **************************************')
        print('GATE - I - sigma I - s/I%')
        for gate,intensity,error in zip(gate_list,gammaray_intensity_list,error_gate_intensity_list):
            if(intensity==0):
                color=bcolors.WHITE
                percentage=0
            elif(error/intensity>0.2 and error/intensity<0.4):
                color=bcolors.WARNING
                percentage=error/intensity
            elif(error/intensity>=0.4):
                color=bcolors.FAIL
                percentage=error/intensity
            else:
                color=bcolors.WHITE
                percentage=error/intensity
            print(f'{color}{gate}: {intensity:.1f}, {error:.1f}, {percentage:.1%}{bcolors.ENDC}')

        if(gammaray_intensity_list.sum()==0):
            color=bcolors.WHITE
            percentage=0
        elif(error_gammaray_intensity/gammaray_intensity_list.sum()>0.2\
            and error_gammaray_intensity/gammaray_intensity_list.sum()<0.4):
            color=bcolors.WARNING
            percentage=error_gammaray_intensity/gammaray_intensity_list.sum()
        elif(error_gammaray_intensity/gammaray_intensity_list.sum()>=0.4):
            color=bcolors.FAIL
            percentage=error_gammaray_intensity/gammaray_intensity_list.sum()
        else:
            color=bcolors.WHITE
            percentage=error_gammaray_intensity/gammaray_intensity_list.sum()
        print(f'\n[{color}{gammaray_energy}: {gammaray_intensity_list.sum():.1f}, {error_gammaray_intensity:.1f}, {percentage:.1%}{bcolors.ENDC}]')

        
    return gammaray_intensity_list.sum(),error_gammaray_intensity


def level_intensity_calculator(level_energy):

    list_of_incoming_gammarays = find_incoming(level_energy)
    list_of_outgoing_gammarays = find_outgoing(level_energy)

    list_of_incoming_intensity = []
    list_of_incoming_errors = []
    list_of_outgoing_intensity = []
    list_of_outgoing_errors = []

    for in_g in list_of_incoming_gammarays:
        res = gammaray_intensity_calc(in_g)
        list_of_incoming_intensity.append(res[0])
        list_of_incoming_errors.append(res[1])

    for ou_g in list_of_outgoing_gammarays:
        res = gammaray_intensity_calc(ou_g)
        list_of_outgoing_intensity.append(res[0])
        list_of_outgoing_errors.append(res[1])

    incoming_intensity = np.asarray(list_of_incoming_intensity).sum()
    outgoing_intensity = np.asarray(list_of_outgoing_intensity).sum()
    list_of_incoming_errors = np.asarray(list_of_incoming_errors)
    list_of_outgoing_errors = np.asarray(list_of_outgoing_errors)
    incoming_error = np.sqrt(np.sum(list_of_incoming_errors**2))
    outgoing_error = np.sqrt(np.sum(list_of_outgoing_errors**2))

    return incoming_intensity,incoming_error,outgoing_intensity,outgoing_error


def level_analyser():

    while ((level_energy:=float(input('LEVEL: '))) not in lvl_scheme[stalc_name].values):
        print(cursor.LINE_UP,end=cursor.LINE_CLEAR)


    list_of_incoming_gammarays = find_incoming(level_energy)
    list_of_outgoing_gammarays = find_outgoing(level_energy)

    print('')
    print('************************************** IN **************************************')
    print('GAMMARAY - I - sigma I - s/I%')
    for in_g in list_of_incoming_gammarays:
        r = gammaray_intensity_calc(in_g)
        if (r[1]/r[0]>0.20 and r[1]/r[0]<0.4):
            color=bcolors.WARNING
        elif (r[1]/r[0]>0.40):
            color=bcolors.FAIL
        else:
            color=bcolors.WHITE
        print(f'{color}{in_g}: {r[0]:.1f}, {r[1]:.1f}, {r[1]/r[0]:.1%}{bcolors.ENDC}')

    print('')
    print('************************************* OUT **************************************')
    print('GAMMARAY - I - sigma I - s/I%')
    for ou_g in list_of_outgoing_gammarays:
        r = gammaray_intensity_calc(ou_g)
        try:
            _ratio=r[1]/r[0]
            if (_ratio>0.20 and _ratio<0.4):
                color=bcolors.WARNING
            elif (_ratio>0.4):
                color=bcolors.FAIL
            else:
                color=bcolors.WHITE
            print(f'{color}{ou_g}: {r[0]:.1f}, {r[1]:.1f}, {_ratio:.1%}{bcolors.ENDC}')
        except:
            print(f'{color}{ou_g}: {r[0]:.1f}, {r[1]:.1f}, {bcolors.ENDC}')
            
    print('')

import time
def gamma_analyser():

    while((gammaray_energy:=float(input('GAMMARAY: '))) not in lvl_scheme[grec_name].values):
        print(cursor.LINE_UP,end=cursor.LINE_CLEAR)

    gammaray_intensity_calc(gammaray_energy,1)
    print(' ')


def analyser():
    
    while (True):
        command=input('COMMAND [l/g/q]: ') 
        if (command not in ['l','g','q']):
            print(cursor.LINE_UP,end=cursor.LINE_CLEAR)
        elif(command == 'q'):
            exit()
        elif command=='l':
            level_analyser() 
        else:
            gamma_analyser()
                 
        

#############################################

#-------------------------------------------#

################## MAIN #####################

if __name__ == '__main__':

    if parser_arguments.analysis is not None:
        analyser()
    else:
        with open('intensity_output.txt','w') as f:

            level_set = sorted(set(lvl_scheme['LevelLITERATURE']))
            print(f'{bcolors.WHITE}{'LEVEL':>6},{'IN':>12},{'ERR':>9},{'%':>5},{'OUT':>12},{'ERR':>9},{'%':>5},{'Chi2':>5}{bcolors.ENDC}',file=f)

            for level in level_set:
                print(f'now doing: {level}')
                r = level_intensity_calculator(level)
                chi = (r[0]-r[2])**2/(r[1]**2+r[3]**2)
                current_line_color=bcolors.WHITE
                if chi>9:
                    current_line_color=bcolors.FAIL
                print(f'{current_line_color}{float(level):6.0f},{r[0]:12.0f},{r[1]:9.0f},{r[1]/r[0]:5.0%},{r[2]:12.0f},{r[3]:9.0f},{r[3]/r[2]:5.0%},{chi:5.0f}{bcolors.ENDC}',file=f)
