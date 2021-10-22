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

'Funciones para el desarrollo'

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

def Area(b,y,inc,m1,m2):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        b (float) base del canal
        y (float) altura del agua
        inc (float) Pendiente de la sección triangular
        m1 (float) Pendiente parte izquierda de un trapecio
        m2 (float) Pendiente parte derecha de un trapecio
    Retorna:
        float: El área de la sección transversal [m^2]
    """
    
    if inc == 0 and m1 == 0 and m2 == 0:
        
        A = b * y
        
    if b == 0:
        
        A = y**2 * inc
            
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
        inc (float) Pendiente de la sección triangular
        m1 (float) Pendiente parte izquierda de un trapecio
        m2 (float) Pendiente parte derecha de un trapecio
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
        inc (float) Pendiente de la sección triangular
        m1 (float) Pendiente parte izquierda de un trapecio
        m2 (float) Pendiente parte derecha de un trapecio
        v1 (float) velocidad de la sección 1 del canal
        z1 (float) Altura del fondo del canal en la sección 1  
        z2 (float) Altura del fondo del canal en la sección 2
        g (float) Aceleración gravitacional, generalmente 9.81 
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    
    if inc == 0 and m1 == 0 and m2 == 0:
        
        ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*(b*y2)**2))+z2)
    
        y2 = solve(ec1)
    
    if b == 0:
        
        ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Qfun(b,y1,inc,m1,m2)**2)/(2*g*(y2**2*inc)**2))+z2)
    
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
        inc (float) Pendiente de la sección triangular
        m1 (float) Pendiente parte izquierda de un trapecio
        m2 (float) Pendiente parte derecha de un trapecio
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
































