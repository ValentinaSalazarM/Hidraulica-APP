# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 18:24:36 2021

@author: JFGJ
"""
'Importar librerias'
import numpy as np
import sympy as sp
from sympy import *
from matplotlib import pyplot as plt

'1/tan30 = 1.73205'
'1/tan60 = 0.57735'

'Variables para la solución del problema'

y2, y = symbols('y2 y')

'Elevación del fondo del canal'


'Datos de entrada'

Figura = 'Rectangular'
Unidades = ''

y1 = 4.5
v1 = 1.25
z1 = 0
z2 = 1.05

'Variables por default necesarias para las funciones'
inc= 1
m1 = 1
m2 = 1

'Gravedad'
g = 9.81


'Datos adicionales dependiente del tipo de figura'

if Figura == "Rectangular":
    
    b = 10

if Figura == "Triangular":
    
    incT = 'alpha'
    
    if incT == "alpha" or incT == "Alpha":
        
        inc = 45
    else:
        
        inc = 1
        
if Figura == "Trapecial":
    
    b = 10
    incTraT = 'alpha'
    
    if incTraT == "alpha" or incTraT == "Alpha":
        
        m1 = 45
        m2 = 45
        
    else:
        
        m1 = 1
        m2 = 1
        
'Funciones para el desarrollo'

def cambio_unidades(unidad,propiedad):
    
    """ Esta realiza el cambio de unidades para las propiedades de la figura\n
        
    Parámetros:
        unidad (string) Unidad en la que se encuentra para propiedad. 
        propiedad (float) Valor de la propiedad que se desea cambiar como base, altura del agua, altura de la base del canal.
    Retorna:
        float: Retorna la propiedad en metros.
    """
    
    if Unidades == 'mm':
        
        temp = propiedad/1000
    
    if Unidades == 'cm':
        
        temp = propiedad/100
    
    if Unidades == 'pulgadas':
        
        temp = propiedad/ 39.37

    if Unidades == 'm':
    
        temp = propiedad
        
    return temp

def Area(b,y,inc,m1,m2):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        b (float) base del canal
        y (float) altura del agua
        inc (float) grados o inclinación de la sección triangular
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
    Retorna:
        float: El área de la sección transversal [m^2]
    """
    
    if Figura == "Rectangular":
        
        A = b * y
        
    if Figura == "Triangular":
        
        if incT == "alpha" or incT == "Alpha":
            
            A = y**2/np.tan(inc*np.pi/180)
            
        else:
            
            A = y**2 * inc
            
    if Figura == "Trapecial":
        
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                A = y*b+y**2/np.tan(np.pi/180*m1)
                
            else:
                
                A = y**2/(2*np.tan(np.pi/180*m1)) + b*y + y**2/(2*np.tan(np.pi/180*m2))  
        else:
            
            if m1 == m2:
                
                A = (b+m1*y)*y
                
            else:
                
                A = m1*y**2/2+b*y+m2*y**2/2 
            
    return A



def Qfun(b,y,inc,m1,m2):
    
    """ Esta función retorna el caudal según la sección transversal\n
        
    Parámetros:
        b (float) base del canal
        y (float) altura del agua
        inc (float) grados o inclinación de la sección triangular
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
    Retorna:
        float: El cuadal de la sección transversal [m^3/s]
    """
    
    Q = v1 * Area(b,y,inc,m1,m2) 
    
    return Q


def Q_en_litros(Q):
    
    """ Esta función retorna el caudal en L/s \n

    Parámetros:
        Q (float) Caudal en m^3/s
    Retorna:
        float: El cuadal de la sección transversal [L/s]
    """
    
    QL = Q *1000
    return QL



def y2fun(y2,b,y1,inc,m1,m2,v1,z1,z2,g):
    
    """ Esta función retorna la altura del agua en la sección dos\n
        
    Parámetros:
        y2 (symbol) variable que se quiere calcular
        b (float) base del canal
        y1 (float) altura del agua en la sección 1
        inc (float) grados o inclinación de la sección triangular
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        v1 (float) velocidad de la sección 1 del canal
        z1 (float) Altura del fondo del canal en la sección 1  
        z2 (float) Altura del fondo del canal en la sección 2
        g (float) Aceleración gravitacional, generalmente 9.81 
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    
    if Figura == "Rectangular":
        
        ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*(b*y2)**2))+z2)
    
        y2 = solve(ec1)
    
    if Figura == "Triangular":
        
        if incT == "alpha" or incT == "Alpha":
            
            ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*(y2**2/np.tan(np.pi/180*inc))**2))+z2)
    
            y2 = solve(ec1)
            
        else:
            ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*(y2**2*inc)**2))+z2)
    
            y2 = solve(ec1)       
    
    if Figura == "Trapecial":
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*(y2*b+y2**2/np.tan(np.pi/180*m1))**2))+z2)
    
                y2 = solve(ec1)
                
            else:
                
                ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*(y2**2/(2*np.tan(np.pi/180*m1)) + b*y2 + y2**2/(2*np.tan(np.pi/180*m2)))**2))+z2)
    
                y2 = solve(ec1) 
        else:
            
            if m1 == m2:
                
                ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*((b+m1*y2)*y2)**2))+z2)
    
                y2 = solve(ec1)
                
            else:
                ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*(m1*y2**2/2+b*y2+m2*y2**2/2)**2))+z2)
            
                y2 = solve(ec1)
    
    return y2 

def grafica2 (b,y1,inc,m1,m2):

    """ Esta función grafica la gráfica de enerigía específica \n
        según la sección transversal
    Parametros:
        b (float) base del canal
        y1 (float) altura del agua
        inc (float) grados o inclinación de la sección triangular
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
    Retorna:
        plot: Gráfica de energía específica[m]
    """

    A = 0    

    x = np.linspace(0,10,10)

    yg = np.linspace(0.2,10,300) 
    
    Ei = yg + (Qfun(b,y1,inc,m1,m2))**2/(2*g*(Area(b,yg,inc,m1,m2))**2)  

    plt.style.use('classic')
    plt.plot(Ei,yg,label = 'S')
    plt.plot(x,x, label = 'E = y', linestyle='dashed')
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend(loc='upper left')
    plt.show()

def imprimir_valores():
    
    """ Esta función retorna los valores del caudal, el área y la gráfica
    Retorna:
        plot: Gráfica de energía específica
        str: Mensaje con los valores de caudal y área
    """
    
    grafica2(b,y1,inc,m1,m2)
    yf = y2fun(y2,b,y1,inc,m1,m2,v1,z1,z2,g)
    
    i=0
    y =[]
    
    while i<len(yf):
        
        y.append(round(yf[i],3))
        i+=1
    
    msg1 = '\nEl área transversal 1 es: '+str(round(Area(b,y1,inc,m1,m2),3)) 
    msg2 = '\nEl cuadal [l/s] es:'+str(round(Q_en_litros(Qfun(b,y1,inc,m1,m2)),4)) 
    msg3 = '\nLos valores de y2 son: '+ str(y)
    if Figura == 'Trapecial':
        msg4 = '\nLa altura final del agua (y2) es: '+str(round(max(yf),2))
        msg6 = '\nEl área transversal 2 es: '+str(round(Area(b,max(yf),inc,m1,m2),3)) 
    else:
        msg4 = '\nLa altura final del agua (y2) es: '+str(y[2])
        msg6 = '\nEl área transversal 2 es: '+str(round(Area(b,y[2],inc,m1,m2),3)) 
    
    temp = msg1 +msg6+ msg2 +msg3 +msg4
    
    return temp


print(imprimir_valores())
































