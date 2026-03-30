from functions import MultGaussPol1,Gauss,FitMultGaussPol1
from random import randrange

import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(80,120,1000)

y=Gauss(x,100,0.74231,4134)+Gauss(x,102,0.54452,10439)+Gauss(x,105,1.1,10000) 
noise=np.asarray([randrange(0,500) for elem in x])
y=y+noise+10*x+100

with open("hist.dat",'w') as file:
    for a,b in zip(x,y):
        print(f'{a} {b}',file=file)


with open("hist.dat",'r') as file:
    hist=np.genfromtxt(file)

res,cov=FitMultGaussPol1(hist,[0,10003,0.7,0.5,1000,1500,0,0],[80,120])
plt.plot(x,y)
plt.plot(x,MultGaussPol1(hist[:,0],*res))
plt.show()
