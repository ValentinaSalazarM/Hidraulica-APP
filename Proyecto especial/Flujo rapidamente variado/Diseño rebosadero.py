# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 00:19:46 2021

@author: JFGJ
"""

NME = 1700

Qmax = 4500

b = 45

Cd = 2.82 

def Hmax(Cd, Qmax,b):
    ''' Calcula la altura máxima \n
    Parámetros:
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
    Retorna:
        float: La altura máxima
    '''
    
    Hmax = (Qmax/(Cd*b))**(2/3)
    
    return Hmax


def ccv(NME,Cd,Qmax,b):
    ''' Calcula la cota de la cresta del vertedero\n
    Parámetros:
        NME (float) Nivel máximo del embalse. 
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
    Retorna:
        float: La cota de la cresta del vertedero
    '''
    ccv = NME - Hmax(Cd, Qmax,b)
    
    return ccv


def Hd(Cd, Qmax,b):
    ''' Calcula la altura de diseño\n
    Parámetros:
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
    Retorna:
        list: Las alturas de diseño divido por los dos valores 1.65 y 1.35
    '''
    
    Hd1 = Hmax(Cd, Qmax,b)/1.65
    
    Hd2 = Hmax(Cd, Qmax,b)/1.35
    
    return Hd1,Hd2

def Qd (Cd, Qmax,b):
    ''' Calcula el caudal de diseño\n
    Parámetros:
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
    Retorna:
        list: los caudales de diseño calculados con las dos alturas de diseño
    '''
    
    Hd1 = float(Hd(Cd, Qmax,b)[0])

    Hd2 = float(Hd(Cd, Qmax,b)[1])
    
    Qd1 = Cd*b*Hd1**(3/2)
    Qd2 = Cd*b*Hd2**(3/2)
    
    return Qd1,Qd2


def Geo(Cd, Qmax,b):
    ''' Calcula el caudal de diseño\n
    Parámetros:
        Cd (float) Coeficiente de descarga.
        Qmax (float) Caudal máximo. 
        b (float) base. 
    Retorna:
        list: la geometría del rebosadero con las dos alturas de diseño
    '''
    Hd1 = float(Hd(Cd, Qmax,b)[0])

    Hd2 = float(Hd(Cd, Qmax,b)[1])
    
    
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
    
    ms1 = 'Para la altura de diseño 1 ('+str(round(Hd1,2))+') es \n r1 es: '+str(round(r1,3)) +' r2 es: '+ str(round(r2,3)) +' x1 es: '+str(round(x1,3))+' x1 es: '+ str(round(x2,3))+' y es: '+str(round(y,3))+'\n'
    
    ms2 = '\nPara la altura de diseño 2 ('+str(round(Hd2,2))+') es \n r1 es: ' +str(round(r12,3))+' r2 es: ' +str(round(r22,3))+' x1 es: '+  str(round(x12,3))+' x1 es: '+str(round(x22,3))+' y es: ' +str(round(y2,3))+'\n'
    
    return ms1+ms2


print(Geo(Cd,Qmax,b))


































