# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 14:37:09 2021

@author: johnf
"""

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
#Varaibles conocidas

ks = 1.5*10**-6

Qd = 1.2

#viscosidad cinemática m^2/s
vi = 1.14*10**-6

#aceleración gravitacional m/s^2
g = 9.81

So = 0.01

Ryd = 85

def cambio_unidades(unidad,propiedad):
    
    """ Esta realiza el cambio de unidades para las propiedades de la figura\n
        
    Parámetros:
        unidad (string) Unidad en la que se encuentra para propiedad. 
        propiedad (float) Valor de la propiedad que se desea cambiar como base, altura del agua, altura de la base del canal.
    Retorna:
        float: Retorna la propiedad en metros.
    """
    
    if unidad == 'mm':
        
        temp = propiedad/1000
    
    if unidad == 'cm':
        
        temp = propiedad/100
    
    if unidad == 'in':
        
        temp = propiedad/ 39.37

    if unidad == 'm':
    
        temp = propiedad
        
    return temp

#Se calcula y
def yfun(Ryd,d,uni):
    """ Calcula la altura del agua según la relacion y/d \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: La altura del agua.
    """

    
    d = cambio_unidades(uni,d)
    y = float(Ryd/100 * d)
    return y

def Thetafun(Ryd,d,uni):
    """ Calcula el ángulo theta de la tuberia \n
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: El ángulo theta de la tuberia.
    """
    
    d = cambio_unidades(uni,d)
    t = np.pi + 2*np.arcsin((yfun(Ryd,d,uni)- d/2)/(d/2))
    return t

#Se calcula el área 
def Areafun(Ryd,d,uni): 
    """ Calcula área transversal del agua \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: El área transversal del agua.
    """
    
    d = cambio_unidades(uni,d)
    A = 1/8 * (Thetafun(Ryd,d,uni)-np.sin(Thetafun(Ryd,d,uni)))*d**2
    return A

#Se calcula el perímetro 
def Perfun(Ryd,d,uni):
    """ Calcula el perimetro de la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: El perimetro de la tuberia.
    """
    d = cambio_unidades(uni,d)
    P = d*Thetafun(Ryd,d,uni)/2
    return P

#Se calcula el espejo de agua
def Tfun (Ryd,d,uni):
    """ Calcula el espejo de agua\n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)            
    Retorna:
        float: El espejo de agua.
    """
    
    d = cambio_unidades(uni,d)
    T = d * np.cos((Thetafun(Ryd,d,uni)-np.pi)/2)
    return T

#Se calcula la profundidad hidráulica 
def Dfun(Ryd,d,uni):
    """ Calcula la profundidad hidráulica\n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d.   
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)                
    Retorna:
        float: La profundidad hidráulica.
    """
    
    D = Areafun(Ryd,d,uni)/Tfun(Ryd,d,uni)
    return D

#Se calcula el rádio hidráulico 
def Rafun(Ryd,d,uni):
    """ Calcula el radio hidráulico de la tuberia \n  
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: El radio hidráulico de la tuberia.
    """
    
    R = Areafun(Ryd,d,uni)/Perfun(Ryd,d,uni)
    return R

#Se calcula la velocidad 
def velofun(Ryd,d,So,ks,vi,g,uni):
    """ Calcula la velocidad del agua\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81   
        uni Unidades propiedades (mm,cm,m,in)     
    Retorna:
        float: La velocidad del agua.
    """
    
    v = -2 * np.sqrt(8*g*Rafun(Ryd,d,uni)*So)*np.log10(((ks)/(14.8*Rafun(Ryd,d,uni)))+((2.51*vi)/(4*Rafun(Ryd,d,uni)*np.sqrt(8*g*Rafun(Ryd,d,uni)*So))))
    return v


#Se calcula el caudal en m^3/s
def Caufun (Ryd,d,So,ks,vi,g,uni):
    """ Calcula el caudal que pasa por la tuberia\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81      
        uni Unidades propiedades (mm,cm,m,in)          
    Retorna:
        float: Caudal que pasa por la tuberia en [m^3/s].
    """
    
    Q = velofun(Ryd,d,So,ks,vi,g,uni)*Areafun(Ryd,d,uni)
    return Q

#Se calcula el caudal en L/s
def CauL(Ryd,d,So,ks,vi,g,uni):
    
    """ Calcula el caudal que pasa por la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d.
        d (float) diametro. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81
        uni Unidades propiedades (mm,cm,m,in)            
    Retorna:
        float: Caudal que pasa por la tuberia en [L/s].
    """
    
    QL = Caufun(Ryd,d,So,ks,vi,g,uni)*1000
    return QL


#Se calcula Froude

def Fr (Ryd,d,So,ks,vi,g,uni):
    """ Calcula el número de Froude \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81      
        uni Unidades propiedades (mm,cm,m,in)              
    Retorna:
        float: Número de Froude (float)
    """
    Fr = velofun(Ryd,d,So,ks,vi,g,uni)/np.sqrt(g*Dfun(Ryd,d,uni))
    return Fr

#Se calcula el esfuerzo cortante tao

def tao(Ryd,d,So,uni):
    """ Calcula el esfuerzo cortante tao\n
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        So (float) inclinación del fondo de la tuberia.  
        uni Unidades propiedades (mm,cm,m,in)              
    Retorna:
        float: Esfuerzo cortante tao(float)
    """
    tao = 9810*Rafun(Ryd,d,uni)*So
    
    return tao

#
def diseno(Ryd,di,So,ks,vi,g,uni):
    uni ='m'
    di = 0
    centinela1 = False
    centinela2 = False
    i = 0
    #Diametros comerciales 
    d = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1, 1.1]
    
    while centinela1 == False:
        
        di = float(d[i])
        
        y = yfun(Ryd,di,uni)
        
        Q = Caufun(Ryd,di,So,ks,vi,g,uni)
        
        if Q > Qd:
            
            centinela1 = True
            
        if Q == Qd:
            
            centinela2 == True
        
        i = i+1
    
    
    while centinela2 == False:
        
        Ryd = y / di *100 
        
        Q = Caufun(Ryd,di,So,ks,vi,g,uni)
        
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
    
    print(di)
    print(Ryd)
    print(round(y,4))
    print(round(Thetafun(Ryd, di,uni),4))
    print(round(Areafun(Ryd,di,uni),4))
    print(round(Perfun(Ryd,di,uni),4))
    print(round(Tfun(Ryd,di,uni),4))
    print(round(Rafun(Ryd,di,uni),4))
    print(round(Dfun(Ryd,di,uni),4))
    print(round(velofun(Ryd,di,So,ks,vi,g,uni),4))
    print(round(CauL(Ryd,di,So,ks,vi,g,uni),4))
    print(round(Fr(Ryd,di,So,ks,vi,g,uni),4))
    print(round(tao(Ryd,di,So,uni),4))
    
    if abs((Fr(Ryd,di,So,ks,vi,g,uni)-1.1)/1.1)<0.01:
        
        
        if Ryd <=70:
            
            return print("Flujo cuasicrítico y cumple porque la relación de llenado es menor o igual a 70%")
        
        else:
            
            return print("Flujo cuasicrítico y no cumple porque la relación de llenado es mayor o igual a 70% \n por favor revisar So ó El material")
    return ''

print(diseno(Ryd,di,So,ks,vi,g,uni))






























