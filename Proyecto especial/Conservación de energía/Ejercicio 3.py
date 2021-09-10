# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 19:55:22 2021

@author: JFGJ
"""

import math
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from sympy import *
b, y1, v1, z1, y2, v2, z2, Q = symbols('b y1 v1 z1 y2 v2 z2 Q')

Q = 55
b = 5
v1 = 1.25
dz = 0.2
g = 9.81

y1 = Q/(v1*b)
q = Q/b


ec1 = Eq(y1+((v1**2)/(2*g))+dz,y2+((q**2)/(2*g*y2**2)))

y2 = solve(ec1)

print(round(y2[0],4))
print(round(y2[1],4))
print(round(y2[2],4))

y2 = y2[2]

def grafica3 (qg):

    x = np.linspace(0,10,10)

    yg = np.linspace(0.2,10,300)
    E = yg + (qg)**2/(2*g*yg**2)    

    plt.style.use('ggplot')
    plt.plot(E,yg,label = 'q')
    plt.plot(x,x)
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend()
    plt.show()
grafica3(q)