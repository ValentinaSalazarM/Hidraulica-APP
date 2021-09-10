# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 18:24:36 2021

@author: JFGJ
"""

import math
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from sympy import *
b, y1, v1, z1, y2, v2, z2, Q = symbols('b y1 v1 z1 y2 v2 z2 Q')

b = 10
y1 = 4.5
v1 = 1.25
z1 = 0
z2 = 1.05
g = 9.81

Q = v1*b*y1

q = Q/b

ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((q**2)/(2*g*y2**2))+z2)

y2 = solve(ec1)

print(round(y2[0],4))
print(round(y2[1],4))
print(round(y2[2],4))

y2 = y2[2]

def grafica2 (v,y):

    x = np.linspace(0,10,10)

    yg = np.linspace(0.2,10,300)
    E = yg + (v*y)**2/(2*g*yg**2)    

    plt.style.use('ggplot')
    plt.plot(E,yg,label = 'q1')
    plt.plot(x,x)
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend()
    plt.show()

grafica2(v1,y1)







































