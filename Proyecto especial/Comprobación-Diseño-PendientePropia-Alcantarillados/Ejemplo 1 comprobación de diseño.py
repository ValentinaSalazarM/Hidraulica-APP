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
    
    if unidad == 'mm':
        
        temp = propiedad/1000
    
    if unidad == 'cm':
        
        temp = propiedad/100
    
    if unidad == 'in':
        
        temp = propiedad/ 39.37

    if unidad == 'm':
    
        temp = propiedad
        
    return temp

## Propiedades Geométricas 

#Se calcula y
def y(Ryd,d,uni):
    
    """ Calcula la altura del agua según la relacion y/d \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: La altura del agua.
    """
    
    d = cambio_unidades(uni,d)
    
    y = Ryd/100 * d
    return y

#Se calcula Theta
def Theta(d,Ryd,uni):
    
    """ Calcula el ángulo theta de la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: El ángulo theta de la tuberia.
    """
    d = cambio_unidades(uni,d)
    
    t = np.pi + 2*np.arcsin((y(Ryd,d,uni) - d/2)/(d/2))
    return t

#Se calcula el área 
def Area(d,Ryd,uni): 
    
    """ Calcula área transversal del agua \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: El área transversal del agua.
    """
    
    d = cambio_unidades(uni,d)
    
    A = 1/8 * (Theta(d,Ryd,uni)-np.sin(Theta(d,Ryd,uni)))*d**2
    return A

#Se calcula el perímetro 
def Per(d,Ryd,uni):
    
    """ Calcula el perimetro de la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: El perimetro de la tuberia.
    """
    d = cambio_unidades(uni,d)
    P = d*Theta(d,Ryd,uni)/2
    return P

#Se calcula el rádio hidráulico 
def Ra(d,Ryd,uni):
    
    """ Calcula el radio hidráulico de la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: El radio hidráulico de la tuberia.
    """
    
    R = Area(d,Ryd,uni)/Per(d,Ryd,uni)
    return R


#Se calcula la velocidad 
def velo(d,Ryd,So,ks,vi,g,uni):
    
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
    
    v = -2 * np.sqrt(8*g*Ra(d,Ryd,uni)*So)*np.log10(((ks)/(14.8*Ra(d,Ryd,uni)))+((2.51*vi)/(4*Ra(d,Ryd,uni)*np.sqrt(8*g*Ra(d,Ryd,uni)*So))))
    return v


#Se calcula el caudal en m^3/s
def Cau (d,Ryd,So,ks,vi,g,uni):
    
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
    
    Q = velo(d,Ryd,So,ks,vi,g,uni)*Area(d,Ryd,uni)
    return Q


#Se calcula el caudal en L/s
def CauL(d,Ryd,So,ks,vi,g,uni):
    
    """ Calcula el caudal que pasa por la tuberia \n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81
        uni Unidades propiedades (mm,cm,m,in)            
    Retorna:
        float: Caudal que pasa por la tuberia en [L/s].
    """
    
    QL = Cau (d,Ryd,So,ks,vi,g,uni)*1000
    return QL


#Se calcula el espejo de agua
def T(d,Ryd,uni):
    
    """ Calcula el espejo de agua\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        uni Unidades propiedades (mm,cm,m,in)            
    Retorna:
        float: El espejo de agua.
    """
    d = cambio_unidades(uni,d)
    T = d * np.cos((Theta(d,Ryd,uni)-np.pi)/2)
    return T


#Se calcula la profundidad hidráulica 
def D(d,Ryd,uni):
    
    """ Calcula la profundidad hidráulica\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d.   
        uni Unidades propiedades (mm,cm,m,in)                
    Retorna:
        float: La profundidad hidráulica.
    """
    
    D = Area(d,Ryd,uni)/T(d,Ryd,uni)
    return D

#Se calcula el número de Froude y Se comprueba que tipo de flujo es

def Fr (d, Ryd, So, ks, vi, g,uni):
    
    """ Calcula el número de Froude \n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81      
        uni Unidades propiedades (mm,cm,m,in)              
    Retorna:
        list: Número de Froude (float), Tipido de flujo (String).
    """
    
    F = velo(d, Ryd, So, ks, vi, g,uni)/(np.sqrt(g*D( d, Ryd,uni)))
    
    if F < 1:
        
        FT = "Subcrítico"
        
    elif F > 1:
        
        FT = "Supercrítico"
    
    else: 
        
        FT = "Crítico"
    
    return F, FT

        
print (Fr(d, Ryd, So, ks, vi, g,'m'))


































