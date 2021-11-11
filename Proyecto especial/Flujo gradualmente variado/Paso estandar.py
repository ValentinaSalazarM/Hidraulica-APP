# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 21:54:23 2021

@author: JFGJ
"""

#Importar librerias'
import math
import numpy as np
import sympy as sp
from sympy import *

#Variables para la solución del problema'

y1,y2,yc = symbols('y1 y2 yc')

##Desarrollo método de paso estandar,
'-----------------------------------------------------------------------------'
'-----------------------------------------------------------------------------'

Q = 35.2
b2 = 8 
L2 = 50
So = 0.0014
n2 = 0.013
g=9.81
m1=0
m2=0

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

def Area(y,b,m1,m2,uni,uni2):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: El área de la sección transversal [m^2]
    """
    
    y = cambio_unidades(uni,y)
    b = cambio_unidades(uni,b)
    m1 = cambio_angulo(uni2,m1)
    m2 = cambio_angulo(uni2,m2)
    
    if m1 == 0 and m2 == 0:
        
        A = b * y
            
    elif b == 0:
        
        A = y**2 * m1
        
    elif b!= 0 and m1 != 0 and m2 != 0:
        
        
        if m1 == m2:
                
            A = (b+m1*y)*y
                
        else:
                
            A = m1*y**2/2+b*y+m2*y**2/2 
            
    return A

def Tfun(y,b,m1,m2,uni,uni2):
    
    """ Esta función retorna el espejo de agua según la sección transversal\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: El espejo de agua de la sección transversal [m]
    """

    y = cambio_unidades(uni,y)
    b = cambio_unidades(uni,b)
    m1 = cambio_angulo(uni2,m1)
    m2 = cambio_angulo(uni2,m2)

    if m1 == 0 and m2 == 0:
        
        T = b

    if b!= 0 and m1 != 0 and m2 != 0:
        
        
        if m1 == m2:
                
            T = b + 2 * (m1*y)
                
        else:
                
            T = b + (m1*y) + (m2*y)

    return T

def yc(Q,yc,b,m1,m2,g,uni,uni2,uni3):
    
    """ Esta función retorna la altura crítica del agua\n
        
    Parámetros:
        Q (float) Caudal.
        yc (symbol) variable que se quiere calcular
        b (float) base del canal en la sección
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
        uni3 (String) Unidades del caudal (m^3/s, l/s)
    Retorna:
        float: La altura crítica del agua [m]
    """
    
    Q = cambio_unidades_Caudal(uni3,Q)
    ec1 = Eq(Q/sqrt(g),(Area(yc, b, m1, m2,uni,uni2)*sqrt(Area(yc, b, m1, m2,uni,uni2)))/sqrt(Tfun(yc, b, m1, m2,uni,uni2)))
            
    yc = solve(ec1)[0]
    
    return yc

def yn(Q,n,So):
    ''' Calcula la altura normal de la sección \n
    Parametros:
        Q (float) Caudal.
        n (float) n de manning.
        So (float) pendiente del fondo del canal.
        uni2 (String) Unidades del caudal (m^3/s, l/s)
    Retorna:
        float: Altura crítica del agua.
    '''
    Q = cambio_unidades_Caudal(uni2,Q)
    
    yn = n*Q/sqrt(So)

print(Area("yc", b2, m1, m2,'m','m',))
#print(yc(Q,'yc',b2,0,0,g,'m','m','m^3/s'))





















































