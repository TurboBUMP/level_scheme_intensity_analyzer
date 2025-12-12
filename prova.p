import numpy as np
import matplotlib.pyplot as plt

efficiency_fit_parameters = np.asarray([-0.423449,
                             -0.832414,
                             -0.714755,
                             +0.274499,
                             +0.034013,
                             -0.0159099])
efficiency_fit_parameters_error = np.asarray([0.0581693,
                                   0.0520197,
                                   0.0258968,
                                   0.0107855,
                                   0.00310721,
                                   0.000739547])


########### FUNCTION DEFINITION #############

# Efficiency function (see MecFarland et al., "Behavior of Several Germanium Detector Full Energy Peak"
# as reference for this function)
# The parameters were fitted with the efficiencyFIT.C ROOT macro.
def efficiency(energy,args):
    efficiency = np.exp(args[0]
            +args[1]*np.log(energy/200)
            +args[2]*np.log(energy/200)**2
            +args[3]*np.log(energy/200)**3
            +args[4]*np.log(energy/200)**4
            +args[5]*np.log(energy/200)**5)
    return efficiency

e = np.arange(50,10000,1)
eff = efficiency(e,[* efficiency_fit_parameters])
low_eff = efficiency(e,[* efficiency_fit_parameters-efficiency_fit_parameters_error])
high_eff = efficiency(e,[* efficiency_fit_parameters+efficiency_fit_parameters_error])
plt.plot(e,low_eff,color='red')
plt.plot(e,high_eff,color='red')
plt.plot(e,eff)
plt.show()
