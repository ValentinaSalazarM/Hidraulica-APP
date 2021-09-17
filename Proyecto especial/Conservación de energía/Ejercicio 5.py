# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 22:25:38 2021

@author: JFGJ
"""

import math
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from sympy import *
b, y1, v1, z1, y2, v2, z2, Q, yin, dz2, y3 = symbols('b y1 v1 z1 y2 v2 z2 Q yin dz2 y3')

y1 = 3.8
v1 = 1.2
g = 9.81

dz = 2.3

q = v1*y1

ec1 = Eq(y1+((q**2)/(2*g*y1**2))-dz,y2+((q**2)/(2*g*y2**2)))

y2 = solve(ec1)

round(y2[0],4)
round(y2[1],4)
round(y2[2],4)

y2 = y2[2]

yc = ((q**2)/(g))**(1/3)

Ec = 3/2*yc

ec2 = Eq(Ec + dz,yin+((q**2)/(2*g*yin**2)))

yin = solve(ec2)

round(yin[0],4)
round(yin[1],4)
round(yin[2],4)

print('\n Cambio del nivel del agua debido al represamiento', round(yin[2],4))


ec3 =  Eq(y1+((q**2)/(2*g*y1**2)),Ec+dz2)

dz2 = solve(ec3)


print('\n dz máximo ', dz2)


ec4 = Eq(y1+((q**2)/(2*g*y1**2)),y3+((q**2)/(2*g*y3**2)))

y3 = solve(ec4)

round(y3[0],4), round(y3[1],4), round(y3[2],4)

print('\n profundidad de la lámina de agua vuelve a la altura original', round(y3[2],4))

def grafica5 (qg):

    x = np.linspace(0,10,10)

    yg = np.linspace(0.2,10,5000)
    E = yg + (qg)**2/(2*g*yg**2)    

    plt.style.use('ggplot')
    plt.plot(E,yg,label = 'q1')
    plt.plot(x,x)
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend()
    plt.show()

grafica5(q)






















