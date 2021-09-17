# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 22:18:04 2021

@author: JFGJ
"""
##Comprobación de diseño

import numpy as np

g = 9.81

pi = np.pi

d = 0.2

ks = 1.5*10**-6

So = 0.001

vi = 1.14*10**-6

Ryd = 93

## Propiedades Geométricas 

#Se calcula y
def y(Ryd,d):
    y = Ryd/100 * d
    return y

y = y(Ryd,d)

#Se calcula Theta
def Theta(y,d):
    t = pi + 2*np.arcsin((y - d/2)/(d/2))
    return t

t = Theta(y,d)

#Se calcula el área 
def Area(t,d):    
    A = 1/8 * (t-np.sin(t))*d**2
    return A

A = Area(t,d)

#Se calcula el perímetro 
def Per(t,d):
    P = d*t/2
    return P

P = Per(t,d)

#Se calcula el rádio hidráulico 
def Ra(A,P):
    
    R = A/P
    return R

R = Ra(A,P)

#Se calcula la velocidad 
def velo(R,So,ks,vi):
    v = -2 * np.sqrt(8*g*R*So)*np.log10(((ks)/(14.8*R))+((2.51*vi)/(4*R*np.sqrt(8*g*R*So))))
    return v

v = velo(R,So,ks,vi)

#Se calcula el caudal en m^3/s
def Cau (v,A):
    
    Q = v*A
    return Q

Q = Cau(v,A)

#Se calcula el caudal en L/s
def CauL(Q):
    QL = Q*1000
    return QL

QL = CauL(Q)

#Se calcula el espejo de agua
def T (d,t):
    T = d * np.cos((t-np.pi)/2)
    return T

T = T(d,t)

#Se calcula la profundidad hidráulica 
def D(A,T):
    D = A/T
    return D

D = D(A,T)

#Se calcula el número de Froud y Se comprueba que tipo de flujo es
FT = ''

def Fr (v,D):
    F = v/(np.sqrt(g*D))
    return F

F = Fr(v,D)


if F < 1:
    
    FT = "Subcrítico"
    
elif F > 1:
    
    FT = "Supercrítico"

else: 
    
    FT = "Crítico"

        
print (FT, F)


































