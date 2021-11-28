# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 00:19:46 2021

@author: JFGJ
"""

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

def cambio_caudal(unidad,propiedad):
    
    """ Esta realiza el cambio de unidades de caudal\n        
    Parámetros:
        unidad (string) Puede ser L/s o m3/s. 
        propiedad (float) Valor del caudal.
    Retorna:
        float: Retorna el caudal en m3/s.
    """
    
    if unidad == 'L':
        
        temp = propiedad/1000
    else:
        temp = propiedad
        
    return temp

def Hmax(Cd, Qmax,b,unib,uniQ):
    ''' Calcula la altura máxima \n
    Parámetros:
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
        unib Unidades de la base del canal (mm,cm,m,in) 
        uniQ Unidades del cuadal (m3,L)
    Retorna:
        float: La altura máxima
    '''
    
    Qmax = cambio_caudal(uniQ, Qmax)
    b = cambio_unidades(unib,b)
    
    Hmax = (Qmax/(Cd*b))**(2/3)
    
    return Hmax


def ccv(NME,Cd,Qmax,b,unib,uniQ,uniNME):
    ''' Calcula la cota de la cresta del vertedero\n
    Parámetros:
        NME (float) Nivel máximo del embalse. 
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
        unib Unidades de la base del canal (mm,cm,m,in) 
        uniQ Unidades del cuadal (m3,L)
        uniNME Unidades del nivel máximo del embalse (mm,cm,m,in)
    Retorna:
        float: La cota de la cresta del vertedero
    '''
    
    NME = cambio_unidades(uniNME,NME)
    
    ccv = NME - Hmax(Cd, Qmax,b,unib,uniQ)
    
    return ccv


def Hd(Cd, Qmax,b,unib,uniQ):
    ''' Calcula la altura de diseño\n
    Parámetros:
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
        unib Unidades de la base del canal (mm,cm,m,in) 
        uniQ Unidades del cuadal (m3,L)
    Retorna:
        list: Las alturas de diseño divido por los dos valores 1.65 y 1.35
    '''
    
    Hd1 = Hmax(Cd, Qmax,b,unib,uniQ)/1.65
    
    Hd2 = Hmax(Cd, Qmax,b,unib,uniQ)/1.35
    
    return Hd1,Hd2

def Qd (Cd, Qmax,b,unib,uniQ):
    ''' Calcula el caudal de diseño\n
    Parámetros:
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
        unib Unidades de la base del canal (mm,cm,m,in) 
        uniQ Unidades del cuadal (m3,L)
    Retorna:
        list: los caudales de diseño calculados con las dos alturas de diseño
    '''
    
    Hd1 = float(Hd(Cd, Qmax,b)[0])

    Hd2 = float(Hd(Cd, Qmax,b)[1])
    
    Qd1 = Cd*b*Hd1**(3/2)
    Qd2 = Cd*b*Hd2**(3/2)
    
    return Qd1,Qd2


def Geo(Cd, Qmax,b,unib,uniQ,uniNME):
    ''' Calcula el caudal de diseño\n
    Parámetros:
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
        unib Unidades de la base del canal (mm,cm,m,in) 
        uniQ Unidades del cuadal (m3,L)
        uniNME Unidades del nivel máximo del embalse (mm,cm,m,in)
    Retorna:
        list: la geometría del rebosadero con las dos alturas de diseño
    '''
    Hd1 = float(Hd(Cd, Qmax,b,unib,uniQ)[0])

    Hd2 = float(Hd(Cd, Qmax,b,unib,uniQ)[1])
    
    ccvt = ccv(NME,Cd,Qmax,b,unib,uniQ,uniNME)
    
    r1 = 0.5 * Hd1
    r2 = 0.2 * Hd1
    x1 = 0.175 * Hd1
    x2 = 0.282 * Hd1
    y = 0.124 * Hd1
    
    r12 = 0.5 * Hd2
    r22 = 0.2 * Hd2
    x12 = 0.175 * Hd2
    x22 = 0.282 * Hd2
    y2 = 0.124 * Hd2
    
    return ccvt,r1,r2,x1,x2,y,r12,r22,x12,x22,y2

unib='m'
uniQ='m3'
uniNME='m'


NME = 1700

Qmax = 4500

b = 45

Cd = 2.82 

print(Geo(Cd,Qmax,b,unib,uniQ,uniNME))


































