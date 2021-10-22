# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 20:04:35 2021

@author: JFGJ
"""
import math
import numpy as np
import sympy as sp
from matplotlib import pyplot as plt
from sympy import *
yin, m, yc, Ec, y2, v2= symbols('yin m yc Ec y2 v2')

'Contracción del canal'
'-----------------------------------------------------------------------------'

'Variables por default necesarias para las funciones'

m1 = 1
m2 = 1

'Gravedad'
g = 9.81

Figura = 'Rectangular'
Unidades = ''
y1 = 3.8
b1 = 16
b2 = 4
v1 = 1.05

'-----------------------------------------------------------------------------'
'Datos adicionales dependiente del tipo de sección'

if Figura == "Trapecial":
    
    incTraT = 'alpha'
    
    if incTraT == "alpha" or incTraT == "Alpha":
        
        m1 = 45
        m2 = 45
        
    else:
        
        m1 = 1
        m2 = 1

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

def Area(y,b,m1,m2):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
    Retorna:
        float: El área de la sección transversal [m^2]
    """
    
    if Figura == "Rectangular":
        
        A = b * y
            
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



def Tfun(y,b,m1,m2):
    
    """ Esta función retorna el espejo de agua según la sección transversal\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
    Retorna:
        float: El espejo de agua de la sección transversal [m]
    """

    if Figura == "Rectangular":
        
        T = b

    if Figura == "Trapecial":
        
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                T = b + 2 * (y/np.tan(np.pi/180*m1))
                
            else:
                
                T = b + (y/np.tan(np.pi/180*m1)) + (y/np.tan(np.pi/180*m2))
        else:
            
            if m1 == m2:
                
                T = b + 2 * (m1*y)
                
            else:
                
                T = b + (m1*y) + (m2*y)

    return T
    

def Qfun(y,b,m1,m2):
    
    """ Esta función retorna el caudal según la sección transversal\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
    Retorna:
        float: El cuadal de la sección transversal [m^3/s]
    """
    
    Q = v1 * Area(y,b,m1,m2) 
    
    return Q


def y2fun(y1,y2,v1,b1,b2,m1,m2,g):
    
    """ Esta función retorna la altura del agua en la sección dos\n
    Parámetros:
        y1 (float) altura del agua de la sección 1
        y2 (symbol) variable que se quiere calcular
        v1 (float) Velocidad de la sección 1
        b1 (float) base del canal en la sección 1
        b2 (float) base del canal en la sección 2
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    
    Q = Qfun(y1,b1,m1,m2)
    
    if Figura == "Rectangular":
        
        ec1 = Eq(y1+((v1**2)/(2*g)),y2+((Q**2)/(2*g*(b2*y2)**2)))
    
        y2 = solve(ec1)  
    
    if Figura == "Trapecial":
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                ec1 = Eq(y1+((v1**2)/(2*g)),y2+((Q**2)/(2*g*(y2*b2+y2**2/np.tan(np.pi/180*m1))**2)))
    
                y2 = solve(ec1)
                
            else:
                
                ec1 = Eq(y1+((v1**2)/(2*g)),y2+((Q**2)/(2*g*(y2**2/(2*np.tan(np.pi/180*m1)) + b2*y2 + y2**2/(2*np.tan(np.pi/180*m2)))**2)))
    
                y2 = solve(ec1) 
        else:
            
            if m1 == m2:
                
                ec1 = Eq(y1+((v1**2)/(2*g)),y2+((Q**2)/(2*g*((b2+m1*y2)*y2)**2)))
    
                y2 = solve(ec1)
                
            else:
                ec1 = Eq(y1+((v1**2)/(2*g)),y2+((Q**2)/(2*g*(m1*y2**2/2+b2*y2+m2*y2**2/2)**2)))
            
                y2 = solve(ec1)
    
    i=0
    y =[]
    
    while i<len(y2):
        
        if im(y2[i])==0:
        
            y.append(round(re(y2[i]),3))
    
        else:
            
            temp = "Fenomeno de choque, se requiere calcular yc\n"
                     
            return temp
            
        i+=1
        
    return y 



def calculo_yc(yc,y1,b1,b2,m1,m2,g):
    
    """ Esta función retorna la altura crítica del agua\n
        
    Parámetros:
        yc (symbol) variable que se quiere calcular
        y1 (float) altura del agua de la sección 1
        b1 (float) base del canal en la sección 1
        b2 (float) base del canal en la sección 2
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
    Retorna:
        float: La altura crítica del agua [m]
    """
    
    Q = Qfun(y1,b1,m1,m2)
    ec1 = Eq(Q/sqrt(g),(Area(yc, b2, m1, m2)*sqrt(Area(yc, b2, m1, m2)))/sqrt(Tfun(yc, b2, m1, m2)))
            
    yc = solve(ec1)[0]
    
    return yc



def calculo_v2(y1,y2,v1,b1,b2,m1,m2,g):
    
    """ Esta función retorna la velocidad del agua en la sección dos\n     
    Parámetros:
        y1 (float) altura del agua de la sección 1
        y2 (symbol) variable que se quiere calcular
        v1 (float) Velocidad de la sección 1
        b1 (float) base del canal en la sección 1
        b2 (float) base del canal en la sección 2
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
    Retorna:
        float: La velocidad del agua en la sección 2 [m]
    """
    
    if y2fun(y1,y2,v1,b1,b2,m1,m2,g) == "Fenomeno de choque, se requiere calcular yc\n":
        ecu = Eq(Qfun(y1,b1,m1,m2),v2*Area(calculo_yc(yc,y1,b1,b2,m1,m2,g),b2,m1,m2))
        v = solve(ecu)
    else:
        if Figura == "Rectangular":
            
            ecu = Eq(Qfun(y1,b1,m1,m2),v2*Area(y2fun(y1,y2,v1,b1,b2,m1,m2,g)[2],b2,m1,m2))
            v = solve(ecu)
        else:
            ecu = Eq(Qfun(y1,b1,m1,m2),v2*Area(max(y2fun(y1,y2,v1,b1,b2,m1,m2,g)),b2,m1,m2))
            v = solve(ecu)
    
    return v


def calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g):

    """ Esta función retorna la velocidad del agua en la sección dos\n     
    Parámetros:
        Ec (symbol) variable que se quiere calcular
        yc (float) altura critica del agua
        y1 (float) altura del agua de la sección 1
        y2 (symbol) variable que se quiere calcular
        v1 (float) Velocidad de la sección 1
        b1 (float) base del canal en la sección 1
        b2 (float) base del canal en la sección 2
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
    Retorna:
        float: La velocidad del agua en la sección 2 [m]
    """
    
    ecu = Eq(Ec,calculo_yc(yc,y1,b1,b2,m1,m2,g) + calculo_v2(y1,y2,v1,b1,b2,m1,m2,g)[0]**2/(2*g))
    
    Ec = solve(ecu)
    
    return Ec

def calculo_yin(Ec,yin,y1,y2,v1,b1,b2,m1,m2,g):
    
    Q = Qfun(y1,b1,m1,m2)
    Ec = calculo_Ec(Ec,yin,y1,y2,v1,b1,b2,m1,m2,g)[0]

    if Figura == "Rectangular":
        
        ec1 = Eq(Ec,yin+((Q**2)/(2*g*(b1*yin)**2)))
    
        yin = solve(ec1)  
    
    if Figura == "Trapecial":
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                ec1 = Eq(Ec,yin+((Q**2)/(2*g*(yin*b1+yin**2/np.tan(np.pi/180*m1))**2)))
    
                yin = solve(ec1)
                
            else:
                
                ec1 = Eq(Ec,yin+((Q**2)/(2*g*(yin**2/(2*np.tan(np.pi/180*m1)) + b1*yin + yin**2/(2*np.tan(np.pi/180*m2)))**2)))
    
                yin = solve(ec1) 
        else:
            
            if m1 == m2:
                
                ec1 = Eq(Ec,yin+((Q**2)/(2*g*((b1+m1*yin)*yin)**2)))
    
                yin = solve(ec1)
                
            else:
                ec1 = Eq(Eq,yin+((Q**2)/(2*g*(m1*yin**2/2+b1*yin+m2*yin**2/2)**2)))
            
                yin = solve(ec1)
    i=0
    y =[]
    
    while i<len(yin):

        y.append(round(re(yin[i]),3))
            
        i+=1
        
    return y


def grafica4 (Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g):

    Q = Qfun(y1,b1,m1,m2)
    EqCri = Eq(m,(0-calculo_yc(yc,y1,b1,b2,m1,m2,g))/(0-calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g)[0]))
    m = solve(EqCri)

    x = np.linspace(0,10,50)

    yg = np.linspace(0.1,10,1000)
    yg2 = np.linspace(0.4,10,1000)
    
    E = yg + (Q**2/(2*g*(Area(yg,b1,m1,m2))**2))
    E2 = yg + (Q**2/(2*g*(Area(yg,b2,m1,m2))**2))
    

    plt.style.use('ggplot')
    plt.plot(E,yg,label = 'S1')
    plt.plot(E2,yg,label = 'S2')
    plt.plot(x,x, label = 'E = y',linestyle='dashed')
    if Figura == "Rectangular":
        plt.plot(x,m*x,label = 'Ec = 3/2 yc', linestyle='dashed')
        
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend()
    plt.show()


def imprimir_valores(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g):
    
    msg1 = '\nArea1 '+ str( Area(y1,b1,m1,m2))
    
    msg2 = '\nCaudal '+ str(Qfun(y1,b1,m1,m2))
    
    msg3 = '\nvalores de y2 '+ str(y2fun(y1,y2,v1,b1,b2,m1,m2,g))
    
    msg4 = '\nvalor de yc'+ str(calculo_yc(yc,y1,b1,b2,m1,m2,g))
    
    msg5 = '\nvalor de Ec'+ str(calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g))

    msg6 = '\nvelocidad en 2 '+ str(calculo_v2(y1,y2,v1,b1,b2,m1,m2,g))   
    
    msg7= '\nNuevo y1 '+ str( max(calculo_yin(Ec,yin,y1,y2,v1,b1,b2,m1,m2,g)))
   
    grafica4(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g)
    
    return msg1 + msg2 + msg3+ msg4+ msg5+ msg6+ msg7
    
print(imprimir_valores(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g))













