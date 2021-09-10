# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 20:04:35 2021

@author: JFGJ
"""
import math
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from sympy import *
b, y1, v1, z1, y2, v2, z2, Q, yin, m = symbols('b y1 v1 z1 y2 v2 z2 Q yin m')

b1 = 16
b2 = 4

v1 = 1.05
y1 = 3.8

Q = 63.84

g = 9.81

q1 = Q/b1
q2 = Q/b2


ec1 = Eq(y1+((q1**2)/(2*g*y1**2)),y2+((q2**2)/(2*g*y2**2)))

y2 = solve(ec1)

#print(round(y2[0],4))
#print(round(y2[1],4))
#print(round(y2[2],4))

y2 = y2[2]

yc = ((q2**2)/(g))**(1/3)

Ec = 3/2*yc

ec2 = Eq(Ec,yin+((q1**2)/(2*g*yin**2)))

yin = solve(ec2)

#print(round(yin[0],4))
#print(round(yin[1],4))
#print(round(yin[2],4))

print(Ec, yc)

EqCri = Eq(m,(0-yc)/(0-Ec))

m = solve(EqCri)

print(m)



yin = yin[2]

def grafica4 (qg1,qg2):

    x = np.linspace(0,10,50)

    yg = np.linspace(0.1,10,1000)
    yg2 = np.linspace(0.4,10,1000)
    
    E = yg + (qg1)**2/(2*g*yg**2) 
    E2 = yg2 + (qg2)**2/(2*g*yg2**2)
    

    plt.style.use('ggplot')
    plt.plot(E,yg,label = 'q1')
    plt.plot(E2,yg,label = 'q2')
    plt.plot(x,m*x,label = 'qc')
    plt.plot(x,x)
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend()
    plt.show()

grafica4(q1,q2)














