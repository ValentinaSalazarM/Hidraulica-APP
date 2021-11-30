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

#Se calcula y
def yfun(Ryd,d,unid):
    """ Calcula la altura del agua según la relacion y/d \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
    Retorna:
        float: La altura del agua.
    """

    
    d = cambio_unidades(unid,d)
    y = float(Ryd/100 * d)
    return y

def Thetafun(Ryd,d,unid):
    """ Calcula el ángulo theta de la tuberia \n
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
    Retorna:
        float: El ángulo theta de la tuberia.
    """
    
    d = cambio_unidades(unid,d)
    t = np.pi + 2*np.arcsin((yfun(Ryd,d,unid)- d/2)/(d/2))
    return t

#Se calcula el área 
def Areafun(Ryd,d,unid): 
    """ Calcula área transversal del agua \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
    Retorna:
        float: El área transversal del agua.
    """
    
    d = cambio_unidades(unid,d)
    A = 1/8 * (Thetafun(Ryd,d,unid)-np.sin(Thetafun(Ryd,d,unid)))*d**2
    return A

#Se calcula el perímetro 
def Perfun(Ryd,d,unid):
    """ Calcula el perimetro de la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
    Retorna:
        float: El perimetro de la tuberia.
    """
    d = cambio_unidades(unid,d)
    P = d*Thetafun(Ryd,d,unid)/2
    return P

#Se calcula el espejo de agua
def Tfun (Ryd,d,unid):
    """ Calcula el espejo de agua\n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: El espejo de agua.
    """
    
    d = cambio_unidades(unid,d)
    T = d * np.cos((Thetafun(Ryd,d,unid)-np.pi)/2)
    return T

#Se calcula la profundidad hidráulica 
def Dfun(Ryd,d,unid):
    """ Calcula la profundidad hidráulica\n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d.   
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: La profundidad hidráulica.
    """
    
    D = Areafun(Ryd,d,unid)/Tfun(Ryd,d,unid)
    return D

#Se calcula el rádio hidráulico 
def Rafun(Ryd,d,unid):
    """ Calcula el radio hidráulico de la tuberia \n  
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: El radio hidráulico de la tuberia.
    """
    
    R = Areafun(Ryd,d,unid)/Perfun(Ryd,d,unid)
    return R

#Se calcula la velocidad 
def velofun(Ryd,d,So,ks,vi,g,unid,uniks,uniS):
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
    v = -2 * np.sqrt(8*g*Rafun(Ryd,d,unid)*So)*np.log10(((ks)/(14.8*Rafun(Ryd,d,unid)))+((2.51*vi)/(4*Rafun(Ryd,d,unid)*np.sqrt(8*g*Rafun(Ryd,d,unid)*So))))
    return v


#Se calcula el caudal en m^3/s
def Caufun (Ryd,d,So,ks,vi,g,unid,uniks,uniS):
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
    
    Q = velofun(Ryd,d,So,ks,vi,g,unid,uniks,uniS)*Areafun(Ryd,d,unid)
    return Q

#Se calcula el caudal en L/s
def CauL(Ryd,d,So,ks,vi,g,unid,uniks,uniS):
    
    """ Calcula el caudal que pasa por la tuberia \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d.
        d (float) diametro. 
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
    
    QL = Caufun(Ryd,d,So,ks,vi,g,unid,uniks,uniS)*1000
    return QL


#Se calcula Froude

def Fr (Ryd,d,So,ks,vi,g,unid,uniks,uniS):
    """ Calcula el número de Froude \n
        
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81      
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
        uniks Unidades de ks (mm,m)
        uniS Unidades de la inclinación (grados,radianes,m/m)
    Retorna:
        float: Número de Froude (float)
    """
    Fr = velofun(Ryd,d,So,ks,vi,g,unid,uniks,uniS)/np.sqrt(g*Dfun(Ryd,d,unid))
    return Fr

#Se calcula el esfuerzo cortante tao

def tao(Ryd,d,So,unid,uniS):
    """ Calcula el esfuerzo cortante tao\n
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (float) diametro.
        So (float) inclinación del fondo de la tuberia.  
        uni Unidades propiedades (mm,cm,m,in)              
    Retorna:
        float: Esfuerzo cortante tao(float)
    """
    So = cambio_unidades(uniS,So)
    
    tao = 9810*Rafun(Ryd,d,unid)*So
    
    return tao

#
def diseno(Ryd,d:list,So,ks,vi,g,unid,uniks,uniS):
    """ Realiza el diseño de la tuberia\n
    Parámetros:
        Ryd (float) Porcentaje de la relación y/d. 
        d (list) diametros.
        So (float) inclinación del fondo de la tuberia.
        ks (float) rugosidad de la tuberia.
        vi (float) viscosidad cinemática del agua.
        g (float) aceleración gravitacional, usualmente 9.81
        unid Unidades del diametro de la tubería (mm,cm,m,in)   
        uniks Unidades de ks (mm,m)
        uniS Unidades de la inclinación (grados,radianes,m/m)
    Retorna:
        float: Esfuerzo cortante tao(float)
    """
    e=''
    ks = cambio_unidades(uniks,ks)
    So = cambio_angulo(uniS,So)
    
    centinela1 = False
    centinela2 = False
    i = 0
    #Diametros comerciales 
    
    while centinela1 == False:

        if i == len(d):
            
            e = 'Error, se necesitan más diametros'
            break
        
        di = float(d[i])
        
        y = yfun(Ryd,di,unid)
        
        Q = Caufun(Ryd,di,So,ks,vi,g,unid,uniks,uniS)
        
        if Q > Qd:
            
            centinela1 = True
            
        elif Q == Qd:
            
            centinela2 == True
        
        i = i+1
    
    if e=='':
            
        while centinela2 == False:
            
            Ryd = y / di *100 
            
            Q = Caufun(Ryd,di,So,ks,vi,g,unid,uniks,uniS)
            
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
    else:
        
        return e
    temp =''
    if abs((Fr(Ryd,di,So,ks,vi,g,unid,uniks,uniS)-1.1)/1.1)<0.01:
        
        
        if Ryd <=70:
            
            temp = "Flujo cuasicrítico y cumple porque la relación de llenado es menor o igual a 70%"
        
        else:
            
            temp = "Flujo cuasicrítico y no cumple porque la relación de llenado es mayor o igual a 70% \n por favor revisar So ó El material"
    
    if temp != '':
        
    
        return temp,di,round(Ryd,4),round(y,4),round(Thetafun(Ryd, di,unid),4),round(Areafun(Ryd,di,unid),4),round(Perfun(Ryd,di,unid),4),round(Tfun(Ryd,di,unid),4),round(Rafun(Ryd,di,unid),4),round(tao(Ryd,di,So,unid,uniS),4),round(Fr(Ryd,di,So,ks,vi,g,unid,uniks,uniS),4),round(CauL(Ryd,di,So,ks,vi,g,unid,uniks,uniS),4),round(velofun(Ryd,di,So,ks,vi,g,unid,uniks,uniS),4),round(Dfun(Ryd,di,unid),4)

    return di,round(Ryd,4),round(y,4),round(Thetafun(Ryd, di,unid),4),round(Areafun(Ryd,di,unid),4),round(Perfun(Ryd,di,unid),4),round(Tfun(Ryd,di,unid),4),round(Rafun(Ryd,di,unid),4),round(tao(Ryd,di,So,unid,uniS),4),round(Fr(Ryd,di,So,ks,vi,g,unid,uniks,uniS),4),round(CauL(Ryd,di,So,ks,vi,g,unid,uniks,uniS),4),round(velofun(Ryd,di,So,ks,vi,g,unid,uniks,uniS),4),round(Dfun(Ryd,di,unid),4)


#Varaibles conocidas
ks = 1.5*10**-6

Qd = 1.2

#viscosidad cinemática m^2/s
vi = 1.14*10**-6

#aceleración gravitacional m/s^2
g = 9.81

So = 0.01

Ryd = 85

d = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 1, 1.1]
#d = [0.25, 0.3, 0.35]
unid='m'
uniks='m'
uniS='m'


print(diseno(Ryd,d,So,ks,vi,g,unid,uniks,uniS))






























