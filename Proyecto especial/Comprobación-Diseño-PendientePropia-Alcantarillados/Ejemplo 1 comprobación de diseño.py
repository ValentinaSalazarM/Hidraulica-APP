# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 22:18:04 2021

@author: JFGJ
"""
##Comprobación de diseño

import numpy as np

Unidades = ''

g = 9.81

d = 0.2

ks = 1.5*10**-6

So = 0.001

vi = 1.14*10**-6

Ryd = 93

## Funciones para el desarrollo 

def cambio_unidades(unidad,propiedad):
    
    """ Esta realiza el cambio de unidades para las propiedades de la figura\n
        
    Parámetros:
        unidad (string) Unidad en la que se encuentra para propiedad. 
        propiedad (float) Valor de la propiedad que se desea cambiar como base, altura del agua, altura de la base del canal.
    Retorna:
        float: Retorna la propiedad en metros.
    """
    
    if Unidades == 'mm':
        
        temp = propiedad/1000
    
    if Unidades == 'cm':
        
        temp = propiedad/100
    
    if Unidades == 'in':
        
        temp = propiedad/ 39.37

    if Unidades == 'm':
    
        temp = propiedad
        
    return temp

## Propiedades Geométricas 

#Se calcula y
def y(Ryd,d):
    
    """ Calcula la altura del agua según la relacion y/d \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
    Retorna:
        float: La altura del agua.
    """
    
    y = Ryd/100 * d
    return y

#Se calcula Theta
def Theta(y,d,Ryd):
    
    """ Calcula el ángulo theta de la tuberia \n
        
    Parámetros:
        y (float) altura del agua.
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
    Retorna:
        float: El ángulo theta de la tuberia.
    """
    
    t = np.pi + 2*np.arcsin((y(Ryd,d) - d/2)/(d/2))
    return t

#Se calcula el área 
def Area(y,d,Ryd): 
    
    """ Calcula área transversal del agua \n
        
    Parámetros:
        y (float) altura del agua.
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
    Retorna:
        float: El área transversal del agua.
    """
    
    A = 1/8 * (Theta(y,d,Ryd)-np.sin(Theta(y,d,Ryd)))*d**2
    return A

#Se calcula el perímetro 
def Per(y,d,Ryd):
    
    """ Calcula el perimetro de la tuberia \n
        
    Parámetros:
        y (float) altura del agua.
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
    Retorna:
        float: El perimetro de la tuberia.
    """
    
    P = d*Theta(y,d,Ryd)/2
    return P

#Se calcula el rádio hidráulico 
def Ra(y,d,Ryd):
    
    """ Calcula el radio hidráulico de la tuberia \n
        
    Parámetros:
        y (float) altura del agua.
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
    Retorna:
        float: El radio hidráulico de la tuberia.
    """
    
    R = Area(y,d,Ryd)/Per(y,d,Ryd)
    return R


#Se calcula la velocidad 
def velo(y,d,Ryd,So,ks,vi,g):
    
    """ Calcula la velocidad del agua\n
        
    Parámetros:
        y (float) altura del agua.
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81        
    Retorna:
        float: La velocidad del agua.
    """
    
    v = -2 * np.sqrt(8*g*Ra(y,d,Ryd)*So)*np.log10(((ks)/(14.8*Ra(y,d,Ryd)))+((2.51*vi)/(4*Ra(y,d,Ryd)*np.sqrt(8*g*Ra(y,d,Ryd)*So))))
    return v


#Se calcula el caudal en m^3/s
def Cau (y,d,Ryd,So,ks,vi,g):
    
    """ Calcula el caudal que pasa por la tuberia\n
        
    Parámetros:
        y (float) altura del agua.
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81        
    Retorna:
        float: Caudal que pasa por la tuberia en [m^3/s].
    """
    
    Q = velo(y,d,Ryd,So,ks,vi,g)*Area(y,d,Ryd)
    return Q


#Se calcula el caudal en L/s
def CauL(y,d,Ryd,So,ks,vi,g):
    
    """ Calcula el caudal que pasa por la tuberia \n
        
    Parámetros:
        y (float) altura del agua.
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81        
    Retorna:
        float: Caudal que pasa por la tuberia en [L/s].
    """
    
    QL = Cau (y,d,Ryd,So,ks,vi,g)*1000
    return QL


#Se calcula el espejo de agua
def T(y,d,Ryd):
    
    """ Calcula el espejo de agua\n
        
    Parámetros:
        y (float) altura del agua.
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
    Retorna:
        float: El espejo de agua.
    """
    
    T = d * np.cos((Theta(y,d,Ryd)-np.pi)/2)
    return T


#Se calcula la profundidad hidráulica 
def D(y,d,Ryd):
    
    """ Calcula la profundidad hidráulica\n
        
    Parámetros:
        y (float) altura del agua.
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d.       
    Retorna:
        float: La profundidad hidráulica.
    """
    
    D = Area(y,d,Ryd)/T(y,d,Ryd)
    return D

#Se calcula el número de Froude y Se comprueba que tipo de flujo es

def Fr (y, d, Ryd, So, ks, vi, g):
    
    """ Calcula el número de Froude \n
        
    Parámetros:
        y (float) altura del agua.
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81        
    Retorna:
        list: Número de Froude (float), Tipido de flujo (String).
    """
    
    F = velo(y, d, Ryd, So, ks, vi, g)/(np.sqrt(g*D(y, d, Ryd)))
    
    if F < 1:
        
        FT = "Subcrítico"
        
    elif F > 1:
        
        FT = "Supercrítico"
    
    else: 
        
        FT = "Crítico"
    
    return F, FT

        
print (Fr(y, d, Ryd, So, ks, vi, g))


































