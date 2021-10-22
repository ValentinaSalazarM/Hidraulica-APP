# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:31:09 2021

@author: JFGJ
"""
'Importar librerias'
import numpy as np
import sympy as sp
from sympy import *

'Variables para la solución del problema'

v2 = symbols('v2')

'Calculo del caudal '
'------------------------------------------------------------------------------'
'Datos de entrada'


y1 = 15
y2 = 3
b=5
inc=1
m1=1
m2=1

'Gravedad'
g = 9.81

'------------------------------------------------------------------------------'
'------------------------------------------------------------------------------'

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
    
    else:
        temp = propiedad
        
    return temp

def Areas(y1,y2,b,inc,m1,m2):
    
    """ Esta función retorna el área transversal según la figura\n
    Parametros: 
        y1 (float) altura de la sección 1 
        y2 (float) altura de la sección 2 
        b (float) base del canal
        inc (int) Pendiente del triangulo
        m1 (int) Pendiente del lado izquierdo del canal 
        m2 (int) Pendiente del lado derecho del canal
    Retorna:
        float: El área de la sección transversal [m^2]
    """
    
    if inc == 0 and m1 == 0 and m2 == 0:
        
        A1 = b * y1
        A2 = b * y2
        
    if b == 0:
        
        A1 = y1**2 * inc
        A2 = y2**2 * inc
            
    else:

        if m1 == m2:
            
            A1 = (b+m1*y1)*y1
            A2 = (b+m1*y2)*y2
            
        else:
            
            A1 = m1*y1**2/2+b*y1+m2*y1**2/2 
            A2 = m1*y2**2/2+b*y2+m2*y2**2/2
        
    return A1,A2

def CaudalSalidafun(y1,y2,v2,b,inc,m1,m2,g):
    
    """Esta función retorna el caudal\n
    
    Parametros:
        y1 (float) altura de la sección 1 
        y2 (float) altura de la sección 2
        v2 (Symbol) velocidad de las sección dos para realizar el cálculo
        b (float) base del canal
        inc (int) Pendiente del triangulo
        m1 (int) Pendiente del lado izquierdo del canal 
        m2 (int) Pendiente de lado derecho del canal
        g (float) Aceleración gravitacional, generalmente 9.81
    Retorna:
        float: El caudal [m^3/s]
    """

    if inc == 0 and m1 == 0 and m2 == 0:
        
        v1 = y2/y1 * v2

        ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))
        
        v2 = round(solve(ecu1)[1],4)
        
        Q = v2 * Areas(y1,y2,b,inc,m1,m2)[1]
        

    if b == 0:
        
        v1 = v2 * y2**2/y1**2
        
        ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

        v2 = round(solve(ecu1)[1],4)
        
        Q = v2 * Areas(y1,y2,b,inc,m1,m2)[1]
        
            
    else:
        
        if m1 == m2:
            
            v1 = v2 * ((b+m1*y2)*y2) * 1/((b+m1*y1)*y1)
        
            ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

            v2 = round(solve(ecu1)[1],4)
            
            Q = v2 * Areas(y1,y2,b,inc,m1,m2)[1]
            
        else:
            
            v1 = v2 * (m1*y2**2/2+b*y2+m2*y2**2/2) * 1/(m1*y1**2/2+b*y1+m2*y1**2/2)
        
            ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

            v2 = round(solve(ecu1)[1],4)
            
            Q = v2 * Areas(y1,y2,b,inc,m1,m2)[1]
        
    return round (Q,4)

def imprimir_valores():
    
    """ Esta función retorna los valores del caudal y las áreas de cada sección
    Retorna:
        str: Mensaje con los valores de caudal y áreas
    """
    
    msg1 = '\nEl área transversal 1 [m^2] es: '+str(round(Areas(y1,y2,b,inc,m1,m2)[0],3)) 
    msg2 = '\nEl área transversal 2 [m^2] es: '+str(round(Areas(y1,y2,b,inc,m1,m2)[1],3)) 
    msg3 = '\nEl cuadal [l/s] es: '+str(round(CaudalSalidafun(y1,y2,v2,b,inc,m1,m2,g)*1000,4)) 
    
    temp = msg1 + msg2 +msg3 
    return temp


print(imprimir_valores())



















