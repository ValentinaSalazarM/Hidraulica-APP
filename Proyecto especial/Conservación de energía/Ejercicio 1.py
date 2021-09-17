# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:31:09 2021

@author: JFGJ
"""
'Importar librerias'
import numpy as np
import sympy as sp
from sympy import *

'1/tan30 = 1.73205'
'1/tan60 = 0.57735'

'Variables para la solución del problema'

v2 = symbols('v2')

'Calculo del caudal'
'------------------------------------------------------------------------------'
'Datos de entrada'

Figura = input("Tipo de figura: ")

y1 = float(input("Altura inicial del agua: "))
y2 = float(input("Altura final del agua: "))

'Gravedad'
g = 9.81

'------------------------------------------------------------------------------'
'Datos adicionales dependiente del tipo de figura'

if Figura == "Rectangular":
    
    b = float(input("Base de la figura: "))

if Figura == "Triangular":
    
    incT = input("Tipo de inclinacio (alpha o m): ")
    
    if incT == "alpha" or incT == "Alpha":
        
        inc = float(input("Inclinación en grados: "))
    else:
        
        inc = float(input("Inclinación (m): "))
        
if Figura == "Trapecial":
    
    b = float(input("Base de la figura: "))
    incTraT = input("Tipo de inclinacio (alpha o m): ")
    
    if incTraT == "alpha" or incTraT == "Alpha":
    
        m1 = float(input("Inclinación lado izquierdo en grados: "))
        m2 = float(input("Inclinación lado derecho en grados: "))
        
    else:
        
        m1 = float(input("Inclinación (m) lado izquierdo: "))
        m2 = float(input("Inclinación (m) lado derecho: "))
      
'------------------------------------------------------------------------------'

def Areas():
    
    """ Esta función retorna el área transversal según la figura\n
    
    Retorna:
        float: El área de la sección transversal [m^2]
    """
    
    if Figura == "Rectangular":
        
        A1 = b * y1
        A2 = b * y2
        
    if Figura == "Triangular":
        
        if incT == "alpha" or incT == "Alpha":
            
            A1 = y1**2/np.tan(np.pi/180*inc)
            A2 = y2**2/np.tan(np.pi/180*inc)
            
        else:
            
            A1 = y1**2 * inc
            A2 = y2**2 * inc
            
    if Figura == "Trapecial":
        
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                A1 = y1*b+y1**2/np.tan(np.pi/180*m1)
                A2 = y2*b+y2**2/np.tan(np.pi/180*m1)
                
            else:
                
                A1 = y1**2/(2*np.tan(np.pi/180*m1)) + b*y1 + y1**2/(2*np.tan(np.pi/180*m2)) 
                A2 = y2**2/(2*np.tan(np.pi/180*m1)) + b*y2 + y2**2/(2*np.tan(np.pi/180*m2)) 
        else:
            
            if m1 == m2:
                
                A1 = (b+m1*y1)*y1
                A2 = (b+m1*y2)*y2
                
            else:
                
                A1 = m1*y1**2/2+b*y1+m2*y1**2/2 
                A2 = m1*y2**2/2+b*y2+m2*y2**2/2
            
    return A1,A2

def CaudalSalidafun(v2):
    
    """Esta función retorna el área transversal según la figura\n
    
    Retorna:
        float: El caudal [m^3/s]
    """

    if Figura == "Rectangular":
        
        v1 = y2/y1 * v2

        ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))
        
        v2 = round(solve(ecu1)[1],4)
        
        Q = v2 * Areas()[1]
        

    if Figura == "Triangular":
        
        if incT == "Alpha" or incT == "alpha":
            
            v1 = v2 * ((y2**2)/(np.tan(np.pi/180*inc))) * ((np.tan(np.pi/180*inc))/(y1**2))
            
            ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

            v2 = round(solve(ecu1)[1],4)
            
            Q = v2 *Areas()[1]
            
        else:
            
            v1 = v2 * y2**2/y1**2
            
            ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

            v2 = round(solve(ecu1)[1],4)
            
            Q = v2 * Areas()[1]
            
            
    if Figura == "Trapecial":
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                v1 = v2 * (y2*b+y2**2/np.tan(np.pi/180*m1)) * 1/(y1*b+y1**2/np.tan(np.pi/180*m1))
            
                ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

                v2 = round(solve(ecu1)[1],4)
                
                Q = v2 * Areas()[1]
                
            else:
                
                v1 = v2 * (y2**2/(2*np.tan(np.pi/180*m1)) + b*y2 + y2**2/(2*np.tan(np.pi/180*m2))) * (1/(y1**2/(2*np.tan(np.pi/180*m1)) + b*y1 + y1**2/(2*np.tan(np.pi/180*m2))))
            
                ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

                v2 = round(solve(ecu1)[1],4)
                
                Q = v2 * Areas()[1]
        else:
            
            if m1 == m2:
                
                v1 = v2 * ((b+m1*y2)*y2) * 1/((b+m1*y1)*y1)
            
                ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

                v2 = round(solve(ecu1)[1],4)
                
                Q = v2 * Areas()[1]
                
            else:
                
                v1 = v2 * (m1*y2**2/2+b*y2+m2*y2**2/2) * 1/(m1*y1**2/2+b*y1+m2*y1**2/2)
            
                ecu1 = Eq(y1 + ((v1)**2/(2*g)),y2 + v2**2/(2*g))

                v2 = round(solve(ecu1)[1],4)
                
                Q = v2 * Areas()[1]
            
    return round (Q,4)

def imprimir_valores():
    
    """ Esta función retorna los valores del caudal y las áreas de cada sección
    Retorna:
        str: Mensaje con los valores de caudal y áreas
    """
    
    msg1 = '\nEl área transversal 1 es: '+str(round(Areas()[0],3)) 
    msg2 = '\nEl área transversal 2 es: '+str(round(Areas()[1],3)) 
    msg3 = '\nEl cuadal [l/s] es: '+str(round(CaudalSalidafun(v2)*1000,4)) 
    
    temp = msg1 + msg2 +msg3 
    return temp


print(imprimir_valores())



















