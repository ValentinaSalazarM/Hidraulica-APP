# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 22:18:04 2021

@author: JFGJ
"""
##Comprobación de diseño

import numpy as np


## Funciones para el desarrollo 

def cambio_angulo(unidad,propiedad):
    
    """ Esta realiza el cambio del angulo\n
        
    Parámetros:
        unidad (string) Puede ser grados o pendiente. 
        propiedad (float) Valor del angulo.
    Retorna:
        float: Retorna el angulo en pendiente (m).
    """
    
    if unidad == 'grados':
        
        temp = 1/np.tan(np.pi/180*propiedad)
        
    if unidad == 'radianes':
        
        temp = 1/np.tan(propiedad)
    
    else:
        temp = propiedad
        
    return temp

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
def y(Ryd,d,unid):
    
    """ Calcula la altura del agua según la relacion y/d \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: La altura del agua.
    """
    
    d = cambio_unidades(unid,d)
    
    y = Ryd/100 * d
    return y

#Se calcula Theta
def Theta(d,Ryd,unid):
    
    """ Calcula el ángulo theta de la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: El ángulo theta de la tuberia.
    """
    d = cambio_unidades(unid,d)
    
    t = np.pi + 2*np.arcsin((y(Ryd,d,unid) - d/2)/(d/2))
    return t

#Se calcula el área 
def Area(d,Ryd,unid): 
    
    """ Calcula área transversal del agua \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: El área transversal del agua.
    """
    
    d = cambio_unidades(unid,d)
    
    A = 1/8 * (Theta(d,Ryd,unid)-np.sin(Theta(d,Ryd,unid)))*d**2
    return A

#Se calcula el perímetro 
def Per(d,Ryd,unid):
    
    """ Calcula el perimetro de la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: El perimetro de la tuberia.
    """
    d = cambio_unidades(unid,d)
    P = d*Theta(d,Ryd,unid)/2
    return P

#Se calcula el rádio hidráulico 
def Ra(d,Ryd,unid):
    
    """ Calcula el radio hidráulico de la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: El radio hidráulico de la tuberia.
    """
    
    R = Area(d,Ryd,unid)/Per(d,Ryd,unid)
    return R


#Se calcula la velocidad 
def velo(d,Ryd,So,ks,vi,g,unid,uniks,uniS):
    
    """ Calcula la velocidad del agua\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81   
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
        uniks Unidades de ks (mm,m)
        uniS Unidades de la inclinación (grados,radianes,m/m)
    Retorna:
        float: La velocidad del agua.
    """
    
    So = cambio_angulo(uniS,So)
    ks = cambio_unidades(uniks,ks)
    v = -2 * np.sqrt(8*g*Ra(d,Ryd,unid)*So)*np.log10(((ks)/(14.8*Ra(d,Ryd,unid)))+((2.51*vi)/(4*Ra(d,Ryd,unid)*np.sqrt(8*g*Ra(d,Ryd,unid)*So))))
    return v


#Se calcula el caudal en m^3/s
def Cau (d,Ryd,So,ks,vi,g,unid,uniks,uniS):
    
    """ Calcula el caudal que pasa por la tuberia\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81      
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
        uniks Unidades de ks (mm,m)
        uniS Unidades de la inclinación (grados,radianes,m/m)
    Retorna:
        float: Caudal que pasa por la tuberia en [m^3/s].
    """
    
    Q = velo(d,Ryd,So,ks,vi,g,unid,uniks,uniS)*Area(d,Ryd,unid)
    return Q


#Se calcula el caudal en L/s
def CauL(d,Ryd,So,ks,vi,g,unid,uniks,uniS):
    
    """ Calcula el caudal que pasa por la tuberia \n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
        uniks Unidades de ks (mm,m)
        uniS Unidades de la inclinación (grados,radianes,m/m)
    Retorna:
        float: Caudal que pasa por la tuberia en [L/s].
    """
    
    QL = Cau (d,Ryd,So,ks,vi,g,unid,uniks,uniS)*1000
    return QL


#Se calcula el espejo de agua
def T(d,Ryd,unid):
    
    """ Calcula el espejo de agua\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        unid Unidades del diametro de la tubería (mm,cm,m,in)        
    Retorna:
        float: El espejo de agua.
    """
    d = cambio_unidades(unid,d)
    T = d * np.cos((Theta(d,Ryd,unid)-np.pi)/2)
    return T


#Se calcula la profundidad hidráulica 
def D(d,Ryd,unid):
    
    """ Calcula la profundidad hidráulica\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d.   
        unid Unidades del diametro de la tubería (mm,cm,m,in)             
    Retorna:
        float: La profundidad hidráulica.
    """
    
    D = Area(d,Ryd,unid)/T(d,Ryd,unid)
    return D

#Se calcula el número de Froude y Se comprueba que tipo de flujo es

def Fr (d, Ryd, So, ks, vi, g,unid,uniks,uniS):
    
    """ Calcula el número de Froude \n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81      
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
        uniks Unidades de ks (mm,m)
        uniS Unidades de la inclinación (grados,radianes,m/m)
    Retorna:
        list: Número de Froude (float), Tipido de flujo (String).
    """
    
    F = velo(d, Ryd, So, ks, vi, g,unid,uniks,uniS)/(np.sqrt(g*D(d,Ryd,unid)))
    
    if F < 1:
        
        FT = "Subcrítico"
        
    elif F > 1:
        
        FT = "Supercrítico"
    
    else: 
        
        FT = "Crítico"
    
    return F, FT


def comprobacion_manning(d,Ryd,So,g,n,unid,uniS):
    
    """ Calcula el caudal, el número de Froude y el tipo de flujo\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        g (float) aceleración gravitacional, usualmente 9.81
        n (float) n de Manning        
        unid Unidades del diametro de la tubería (mm,cm,m,in)
        uniS Unidades de la inclinación (grados,radianes,m/m)
    Retorna:
        list: Caudal (float), Número de Froude (float), Tipido de flujo (String).
    """
    
    So = cambio_angulo(uniS,So)
    d = cambio_unidades(unid,d)
    
    R = Ra(d, Ryd, unid)
    A = Area(d, Ryd, unid)
    
    v = (1/n)*(R**(2/3))*(So**(1/2))
    
    Q = v*A
    
    Fr = v/np.sqrt(g*D(d, Ryd, unid))
    
    if Fr < 1:
        
        FT = "Subcrítico"
        
    elif Fr > 1:
        
        FT = "Supercrítico"
    
    else: 
        
        FT = "Crítico"
    
    return Q,Fr,FT


def valores_Darcy(d, Ryd, So, ks, vi, g,unid,uniks,uniS):
    
    """ Calcula el caudal, el número de Froude y el tipo de flujo\n
        
    Parámetros:
        d (float) diametro.
        Ryd (float) Porcentaje de la relación y/d. 
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81      
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
        uniks Unidades de ks (mm,m)
        uniS Unidades de la inclinación (grados,radianes,m/m)
    Retorna:
        list: Caudal (float), Número de Froude (float), Tipido de flujo (String).
    """
    F = Fr(d, Ryd, So, ks, vi, g,unid,uniks,uniS)
    Q = CauL(d, Ryd, So, ks, vi, g, unid, uniks, uniS)
    
    return Q,F
    

g = 9.81
d = 0.2
ks = 1.5*10**-6
So = 0.001
vi = 1.14*10**-6
Ryd = 93    
n=0.00013
unid='m'
uniks='m'
uniS='m'


print(comprobacion_manning(d,Ryd,So,g,n,unid,uniS))
print (valores_Darcy(d, Ryd, So, ks, vi, g,unid,uniks,uniS))


































