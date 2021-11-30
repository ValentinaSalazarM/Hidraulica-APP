# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 09:38:10 2021

@author: JFGJ
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 09:39:36 2021

@author: JFGJ
"""

import numpy as np
import sympy as sp
from sympy import *

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

def cambio_unidades_Caudal(unidad,caudal):
    
    """ Esta realiza el cambio de unidades del caudal\n
    Parámetros:
        unidad (string) Unidad en la que se encuentra el caudal. 
        caudal (float) Caudal.
    Retorna:
        float: Retorna la propiedad en metros.
    """
    
    if unidad == 'L':
        
        temp = caudal/1000
    else:
        temp = caudal
        
    return temp

def Energia_Inicial (yo, delta_y,uniy,unidy):
    
    """ Calcula la energía inical\n
    Parámetros:
        yo (float) altura inicial 
        delta_y (float) diferencia en la altura inicial y el fondo de la piscina
        uniy unidades de la altura inicial (mm,cm,m,in)
        unidy unidades de delta y (mm,cm,m,in)
    Retorna:
        float: Energía inicial.
    """
    
    yo = cambio_unidades(uniy,yo)
    delta_y = cambio_unidades(unidy,delta_y)
    
    Eo = yo + delta_y
    
    return Eo 

def Caudal_base(Q,b,unib,uniQ):
    
    """ Calcula el caudal divido por la base\n
    Parámetros:
        Q (float) Caudal.
        b (float) base del canal
        unib unidades de la base del canal (mm,cm,m,in)
        uniQ unidades de del caudal (m3,L)
    Retorna:
        float: Caudal divido por la base.
    """
    
    Q = cambio_unidades_Caudal(uniQ,Q)
    b = cambio_unidades(unib,b)
    
    q = Q/b
    
    return q

def y1(yo,delta_y,Q,b,g,S,uniy,unidy,uniQ,unib,uniS):
    
    """ Calcula la altura al final de la caída\n
    Parámetros:
        yo (float) altura inicial
        delta_y (float) diferencia en la altura inicial y el fondo de la piscina
        Q (float) Caudal.
        b (float) base del canal
        g (float) aceleración gravitacional, usualmente 9.81      
        S (float) inclinación de la caída.
        uniy unidades de la altura inicial (mm,cm,m,in)
        unidy unidades de delta y (mm,cm,m,in)
        uniQ unidades de del caudal (m3,L)
        unib unidades de la base del canal (mm,cm,m,in)
        uniS unidades de la inclinación (grados,radianes,m)
    Retorna:
        float: altura al final de la caída.
    """
    y = symbols('y')

    E = Energia_Inicial(yo,delta_y,uniy,unidy)
    q = Caudal_base(Q,b,unib,uniQ)
    S = cambio_angulo(uniS,S)   
    
    ecu = Eq(E,y+q**2/(2*g*y**2*S**2))
    
    y1 = round(re(solve(ecu)[1]),3)
    
    return y1

def yo(yo,delta_y,Q,b,g,S,uniy,unidy,uniQ,unib,uniS):
    
    """ Calcula la altura inicial\n
    Parámetros:
        yo (float) altura inicial
        delta_y (float) diferencia en la altura inicial y el fondo de la piscina
        Q (float) Caudal.
        b (float) base del canal
        g (float) aceleración gravitacional, usualmente 9.81      
        S (float) inclinación de la caída.
        uniy unidades de la altura inicial (mm,cm,m,in)
        unidy unidades de delta y (mm,cm,m,in)
        uniQ unidades de del caudal (m3,L)
        unib unidades de la base del canal (mm,cm,m,in)
        uniS unidades de la inclinación (grados,radianes,m)
    Retorna:
        float: altura inicial.
    """
    y = symbols('y')

    E = Energia_Inicial(yo,delta_y,uniy,unidy)
    q = Caudal_base(Q,b,unib,uniQ)
    S = cambio_angulo(uniS,S)   
    
    ecu = Eq(E,y+q**2/(2*g*y**2*S**2))
    
    yo = round(re(solve(ecu)[2]),3)
    
    return yo

def y2(yo,delta_y,Q,b,g,S,uniy,unidy,uniQ,unib,uniS):
    
    """ Calcula y2\n
    Parámetros:
        yo (float) altura inicial
        delta_y (float) diferencia en la altura inicial y el fondo de la piscina
        Q (float) Caudal.
        b (float) base del canal
        g (float) aceleración gravitacional, usualmente 9.81      
        S (float) inclinación de la caída.
        uniy unidades de la altura inicial (mm,cm,m,in)
        unidy unidades de delta y (mm,cm,m,in)
        uniQ unidades de del caudal (m3,L)
        unib unidades de la base del canal (mm,cm,m,in)
        uniS unidades de la inclinación (grados,radianes,m)
    Retorna:
        float: y2.
    """
    y = symbols('y')

    y1_temp = y1(yo,delta_y,Q,b,g,S,uniy,unidy,uniQ,unib,uniS)
    q = Caudal_base(Q,b,unib,uniQ)
    
    ecu = Eq(y,(y1_temp/2)*(sqrt(1+8*(q**2/(g*y1_temp**3)))-1))
    
    y2_temp = float(solve(ecu)[0])
    
    return round(y2_temp,3)


def delta_y_i(sigma,yn,yo,delta_y,Q,b,g,S,uniyn,uniy,unidy,uniQ,unib,uniS):
    
    """ Calcula delta y en cada iteración\n
    Parámetros:
        sigma (float) sigma elegido por el usuario.
        yn (float) altura normal.
        yo (float) altura inicial
        delta_y (float) diferencia en la altura inicial y el fondo de la piscina
        Q (float) Caudal.
        b (float) base del canal
        g (float) aceleración gravitacional, usualmente 9.81      
        S (float) inclinación de la caída.
        uniyn unidades de la altura normal (mm,cm,m,in)
        uniy unidades de la altura inicial (mm,cm,m,in)
        unidy unidades de delta y (mm,cm,m,in)
        uniQ unidades de del caudal (m3,L)
        unib unidades de la base del canal (mm,cm,m,in)
        uniS unidades de la inclinación (grados,radianes,m)
    Retorna:
        float: y2.
    """
    y = symbols('y')

    yn = cambio_unidades(uniyn,yn)
    
    y2_temp = y2(yo,delta_y,Q,b,g,S,uniy,unidy,uniQ,unib,uniS)
    
    delta_y_temp = sigma*y2_temp - yn
    
    return delta_y_temp
    
def ciclo_Fr(sigma, yn, yo, delta_y, Q, b, g, S,uniyn,uniy,unidy,uniQ,unib,uniS):
    
    """ Realiza las iteraciones necesarias para calcular el tipo de piscina\n
    Parámetros:
        sigma (float) sigma elegido por el usuario.
        yn (float) altura normal.
        yo (float) altura inicial
        delta_y (float) diferencia en la altura inicial y el fondo de la piscina
        Q (float) Caudal.
        b (float) base del canal
        g (float) aceleración gravitacional, usualmente 9.81      
        S (float) inclinación de la caída.
        uniyn unidades de la altura normal (mm,cm,m,in)
        uniy unidades de la altura inicial (mm,cm,m,in)
        unidy unidades de delta y (mm,cm,m,in)
        uniQ unidades de del caudal (m3,L)
        unib unidades de la base del canal (mm,cm,m,in)
        uniS unidades de la inclinación (grados,radianes,m)
    Retorna:
        list: delta y, Energia inicial, y1, y2, delta y i+1, error, velocidad, froude y tipo de piscina.
    """
    
    Q = cambio_unidades_Caudal(uniQ,Q)
    b = cambio_unidades(unib,b)
    
    delta_y = 0
    centineta = False
    
    while centineta == False:
        
        E = Energia_Inicial(yo, delta_y, uniy,unidy)
        y1_temp = y1(yo, delta_y, Q, b, g, S,uniy,unidy,uniQ,unib,uniS)
        y2_temp = y2(yo, delta_y, Q, b, g, S,uniy,unidy,uniQ,unib,uniS)
        delta_y_i_temp = delta_y_i(sigma, yn, yo, delta_y, Q, b, g, S,uniyn,uniy,unidy,uniQ,unib,uniS)
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
    
    return delta_y,E,y1_temp,y2_temp,delta_y_i_temp,er,v1,round(Fr1,3),msg

uniy='m'
unidy='m'
uniQ='m3'
unib='m'
uniS='m'
uniyn='m'

Q = 375
b = 20
S = 0.7
sigma = 1.1
yn = 3.45
g = 9.81
yos=21
delta_y=0

print(ciclo_Fr(sigma,yn,yos,delta_y,Q,b,g,S,uniyn,uniy,unidy,uniQ,unib,uniS))

















































