# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 09:39:36 2021

@author: JFGJ
"""

import numpy as np
import sympy as sp
from sympy import *

y = symbols('y')


Q = 375
b = 20
S = 0.7
sigma = 1.1
yn = 3.45
g = 9.81

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

def cambio_unidades_Caudal(unidad,caudal):
    
    """ Esta realiza el cambio de unidades del caudal\n
    Parámetros:
        unidad (string) Unidad en la que se encuentra el caudal. 
        caudal (float) Caudal.
    Retorna:
        float: Retorna la propiedad en metros.
    """
    
    if unidad == 'm^3/s':
        
        temp = caudal
    
    if unidad == 'l/s':
        
        temp = caudal/1000

    return temp

def Energia_Inicial (yo, delta_y,uni):
    
    yo = cambio_unidades(uni,yo)
    delta_y = cambio_unidades(uni,delta_y)
    
    Eo = yo + delta_y
    
    return Eo 

def Caudal_base(Q,b,uni,uni2):
    
    Q = cambio_unidades_Caudal(uni2,Q)
    b = cambio_unidades(uni,b)
    
    q = Q/b
    
    return q

def y1(y,yo,delta_y,Q,b,g,S,uni,uni2):
    
    E = Energia_Inicial(yo,delta_y,uni)
    q = Caudal_base(Q,b,uni,uni2)
    
    ecu = Eq(E,y+q**2/(2*g*y**2*S**2))
    
    y1 = round(re(solve(ecu)[1]),3)
    
    return y1

def yo(y,yo,delta_y,Q,b,g,S,uni,uni2):
    
    E = Energia_Inicial(yo,delta_y,uni)
    q = Caudal_base(Q,b,uni,uni2)
    
    ecu = Eq(E,y+q**2/(2*g*y**2*S**2))
    
    yo = round(re(solve(ecu)[2]),3)
    
    return yo

def y2(y,yo,delta_y,Q,b,g,S,uni,uni2):
    
    y1_temp = y1(y,yo,delta_y,Q,b,g,S,uni,uni2)
    q = Caudal_base(Q,b,uni,uni2)
    
    ecu = Eq(y,(y1_temp/2)*(sqrt(1+8*(q**2/(g*y1_temp**3)))-1))
    
    y2_temp = float(solve(ecu)[0])
    
    return round(y2_temp,3)


def delta_y_i(sigma,yn,y,yo,delta_y,Q,b,g,S,uni,uni2):
    
    y2_temp = y2(y,yo,delta_y,Q,b,g,S,uni,uni2)
    
    delta_y_temp = sigma*y2_temp - yn
    
    return delta_y_temp
    
def ciclo_Fr(sigma, yn, y, yo, delta_y, Q, b, g, S, uni, uni2):
    
    Q = cambio_unidades_Caudal(uni2,Q)
    b = cambio_unidades(uni,b)
    
    delta_y = 0
    centineta = False
    
    while centineta == False:
        
        E = Energia_Inicial(yo, delta_y, uni)
        y1_temp = y1(y, yo, delta_y, Q, b, g, S, uni, uni2)
        y2_temp = y2(y, yo, delta_y, Q, b, g, S, uni, uni2)
        delta_y_i_temp = delta_y_i(sigma, yn, y, yo, delta_y, Q, b, g, S, uni, uni2)
        er = abs(delta_y-delta_y_i_temp)
        delta_y = delta_y + er
        
        if er < 0.001:
            
            centineta = True
        
    v1 = Q/(b*y1_temp)
    
    Fr1 = Q/(b*y1_temp*sqrt(g*y1_temp))
    
    if Fr1<2.5:
        
        msg = 'No requiere piscina de disipación'
    
    elif Fr1 >=2.5 and Fr1<4.5:
        
        msg = "Tipo IV ó IVa "
        
    elif Fr1>4.5 and v1 < 18.3:
        
        msg = "Tipo III"
    
    elif Fr1>4.5 and v1 > 18.3:
        
        msg = "Tipo II"
    
    return round(Fr1,3),msg



#print(y2(y,21,0,375,20,9.81,0.7,'m','m^3/s'))
#print(delta_y_i(sigma,yn,y,21,0,375,20,9.81,0.7,'m','m^3/s'))
#print(ciclo_Fr(sigma,yn,y,21,0,375,20,9.81,0.7,'m','m^3/s'))


















































