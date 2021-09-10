# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 23:04:58 2021

@author: JFGJ
"""
##Diseño de tuberia simple 

import numpy as np
import sympy as sp
import math as mt 
from sympy import *
yn = symbols('yn')
#Diametros comerciales 

d = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1, 1.1]

#Varaibles conocidas

di = 0
centinela1 = False
centinela2 = False
i = 0
j = 0

ks = 1.5*10**-6

Qd = 1.2

#viscosidad cinemática m^2/s
vi = 1.14*10**-6

g = 9.81

So = 0.01

Ryd = 85

#Se calcula y
def yfun(Ryd,d):
    y = float(Ryd/100 * d)
    return y

def Thetafun(y,d):
    t = np.pi + 2*np.arcsin((y - d/2)/(d/2))
    return t

#Se calcula el área 
def Areafun(t,d):    
    A = 1/8 * (t-np.sin(t))*d**2
    return A

#Se calcula el perímetro 
def Perfun(t,d):
    P = d*t/2
    return P

#Se calcula el espejo de agua
def Tfun (d,t):
    T = d * np.cos((t-np.pi)/2)
    return T

#Se calcula la profundidad hidráulica 
def Dfun(A,T):
    D = A/T
    return D

#Se calcula el rádio hidráulico 
def Rafun(A,P):
    
    R = A/P
    return R

#Se calcula la velocidad 
def velofun(R,So,ks,vi):
    v = -2 * np.sqrt(8*g*R*So)*np.log10(((ks)/(14.8*R))+((2.51*vi)/(4*R*np.sqrt(8*g*R*So))))
    return v


#Se calcula el caudal en m^3/s
def Caufun (v,A):
    
    Q = v*A
    return Q

#Se calcula Froude

def Fr (v,D):
    
    Fr = v/np.sqrt(g*D)
    return Fr

#Se calcula el esfuerzo cortante tao

def tao(R,So):
    
    tao = 9810*R*So
    
    return tao

#

while centinela1 == False:
    
    di = float(d[i])
    
    y = yfun(Ryd,di)

    t = Thetafun(y,di) 
    
    A = Areafun(t,di)
    
    P = Perfun(t,di)
    
    T = Tfun(di,t)
    
    D = Dfun(A,T)
    
    R = Rafun(A,P)
    
    v = velofun(R,So,ks,vi)
    
    Q = Caufun(v,A)
    
    if Q > Qd:
        
        centinela1 = True
        
    if Q == Qd:
        
        centinela2 == True
    
    i = i+1


while centinela2 == False:
    
    Ryd = y / di *100 
    
    t = Thetafun(y,di) 
    
    A = Areafun(t,di)
    
    P = Perfun(t,di)
    
    T = Tfun(di,t)
    
    D = Dfun(A,T)
    
    R = Rafun(A,P)
    
    v = velofun(R,So,ks,vi)
    
    Q = Caufun(v,A)
    
    if Q > Qd: 
        
        if abs((Qd-Q)/Qd)<0.0001:
            
            centinela2 == True
            
            break 
        
        y = y-0.0001
    
    if Q < Qd:
        
        if abs((Qd-Q)/Qd)<0.0001:
            
            centinela2 == True
        
            break 
        
        y = y+0.0001



print(round(Q,4), Qd, round(y,4), di, round(Fr(v,D),4), round(tao(R,So),4), Ryd)

if abs((Fr(v,D)-1.1)/1.1)<0.01:
    
    
    if Ryd <=70:
        
        print("Flujo cuasicrítico y cumple porque la relación de llenado es menor o igual a 70%")
    
    else:
        
        print("Flujo cuasicrítico y no cumple porque la relación de llenado es mayor o igual a 70% \n por favor revisar So ó El material")

































