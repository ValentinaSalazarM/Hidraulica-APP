# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 00:19:46 2021

@author: JFGJ
"""

NME = 1700

Qmax = 4500

b = 45

Cd = 2.82 

def Hmax(Cd, Qmax):
    
    Hmax = (Qmax/(Cd*b))**(2/3)
    
    return Hmax

Hmax = Hmax(Cd, Qmax)

def ccv(Hmax):
    
    ccv = NME - Hmax
    
    return ccv

ccv = ccv(Hmax)

def Hd(Hmax):
    
    Hd1 = Hmax/1.65
    
    Hd2 = Hmax/1.35
    
    return Hd1,Hd2

Hd1 = float(Hd(Hmax)[0])

Hd2 = float(Hd(Hmax)[1])

def Qd (Cd,b,H):
    
    Qd = Cd*b*H**(3/2)
    
    return Qd

Qd1 = Qd(Cd,b,Hd1)

Qd2 = Qd(Cd,b,Hd2)

def Geo(Hd):
    
    r1 = 0.5 * Hd
    r2 = 0.2 * Hd
    x1 = 0.175 * Hd
    x2 = 0.282 * Hd
    y = 0.124 * Hd
    
    return round(r1,3), round(r2,3),  round(x1,3),  round(x2,3), round(y,3)

geo1 = Geo(Hd1)

geo2 = Geo(Hd2)

print(geo1)
print(geo2)


































