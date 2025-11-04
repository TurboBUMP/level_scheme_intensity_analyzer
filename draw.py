#!/bin/python3

import matplotlib.pyplot as plt
import numpy as np

filename = input('Filename: ')

h = np.genfromtxt(filename)
plt.plot(h[:,0],h[:,1])
plt.show()
