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
b, y1, v1, z1, y2, v2, z2, Q, yin, m, yc = symbols('b y1 v1 z1 y2 v2 z2 Q yin m yc')

'Contracción del canal'
'-----------------------------------------------------------------------------'
'Datos de entrada'
'''
Figura = input("Tipo de figura: ")

y1 = float(input("Altura inicial del agua (y1): "))
b1 = float(input("Base inicial del canal (b1): "))
b2 = float(input("Base final del canal (b2): "))
v1 = float(input("Velocidad inicial del agua (v1): "))
'''
'Variables por default necesarias para las funciones'
inc= 1
m1 = 1
m2 = 1

'Gravedad'
g = 9.81

Figura = 'Rectangular'
y1 = 3.8
b1 = 16
b2 = 10
v1 = 1.05

'-----------------------------------------------------------------------------'
'Datos adicionales dependiente del tipo de figura'

if Figura == "Trapecial":
    
    incTraT = input("Tipo de inclinacio (alpha o m): ")
    
    if incTraT == "alpha" or incTraT == "Alpha":
        
        m1 = float(input("Inclinación lado izquierdo en grados: "))
        m2 = float(input("Inclinación lado derecho en grados: "))
        
    else:
        
        m1 = float(input("Inclinación (m) lado izquierdo: "))
        m2 = float(input("Inclinación (m) lado derecho: "))

def Area(y,b,inc,m1,m2):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
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

def Qfun(y,b,inc,m1,m2):
    
    """ Esta función retorna el caudal según la sección transversal\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        inc (float) grados o inclinación de la sección triangular
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
    Retorna:
        float: El cuadal de la sección transversal [m^3/s]
    """
    
    Q = v1 * Area(y,b,inc,m1,m2) 
    
    return Q

def y2fun(y2):
    
    """ Esta función retorna la altura del agua en la sección dos\n
        
    Parámetros:
        y1 (symbol) variable que se quiere calcular
        y2 (symbol) variable que se quiere calcular
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    Q = Qfun(y1,b1,inc,m1,m2)
    
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
            
            y.append(round(y2[i],3))
        i+=1
        
    return y 

print(y2fun(y2))

def calculo_v2():
    
    i=0
    
    while i<len(y2fun(y2))-1:
        
        if im(y2fun(y2)[i]) == 0 :
            ecu = Eq(Qfun(y1,b1,inc,m1,m2),v2*Area(y2fun(y2)[2],b2,inc,m1,m2))
            v = solve(ecu)
        else:
            return "Error, fenomeno de choque"
        i+=1
    return v

print(calculo_v2())

def calculo_yc(yc):
    
    
    if calculo_v2() == "Error, fenomeno de choque":
        return "Error, fenomeno de choque"
    
    v2 = calculo_v2()[0]
    y2 = y2fun(yc)[len(y2fun(yc))-1]
    
    if Figura == "Rectangular":
        
        ec1 = Eq(yc,((v2**2*(b2*y2)**2)/(b2**2*g))**(1/3))
    
        yc = solve(ec1)  
    
    if Figura == "Trapecial":
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                ec1 = Eq(yc, ((v2**2*(y2*b2+y2**2/np.tan(np.pi/180*m1))**2)/(b2**2*g))**(1/3))
    
                yc = solve(ec1)
                
            else:
                
                ec1 = Eq(yc,((v2**2*(y2**2/(2*np.tan(np.pi/180*m1)) + b2*y2 + y2**2/(2*np.tan(np.pi/180*m2)))**2)/(b2**2*g))**(1/3))
    
                yc = solve(ec1) 
        else:
            
            if m1 == m2:
                
                ec1 = Eq(yc,((v2*((b2+m1*y2)*y2)**2)/(b2**2*g))**(1/3))
    
                yc = solve(ec1)
                
            else:
                ec1 = Eq(yc,((v2*(m1*y2**2/2+b2*y2+m2*y2**2/2)**2)/(b2**2*g))**(1/3))
            
                yc = solve(ec1)
    return yc

print(calculo_yc(yc))

'¿Cómo calculo yc para una sección que no sea rectangular?'
'v depende de y2 pero y2 puede ser imaginario'
def calculo_Ec(yc):
    
    try:
        Ec = (3/2)*calculo_yc(yc)[0]
    except:
        return print("Error")
        
    return Ec

print(calculo_Ec(yc))

def calculo_yin(yin):
    
    Q = Qfun(y1,b1,inc,m1,m2)
    Ec = calculo_Ec(yin)
    
    if Figura == "Rectangular":
        
        ec1 = Eq(Ec,yin+((Q**2)/(2*g*(b2*yin)**2)))
    
        yin = solve(ec1)  
    
    if Figura == "Trapecial":
        
        if incTraT == "alpha" or incTraT == "Alpha":
            
            if m1 == m2:
                
                ec1 = Eq(Ec,yin+((Q**2)/(2*g*(yin*b2+yin**2/np.tan(np.pi/180*m1))**2)))
    
                yin = solve(ec1)
                
            else:
                
                ec1 = Eq(Ec,yin+((Q**2)/(2*g*(yin**2/(2*np.tan(np.pi/180*m1)) + b2*yin + yin**2/(2*np.tan(np.pi/180*m2)))**2)))
    
                yin = solve(ec1) 
        else:
            
            if m1 == m2:
                
                ec1 = Eq(Ec,yin+((Q**2)/(2*g*((b2+m1*yin)*yin)**2)))
    
                yin = solve(ec1)
                
            else:
                ec1 = Eq(Eq,yin+((Q**2)/(2*g*(m1*yin**2/2+b2*yin+m2*yin**2/2)**2)))
            
                yin = solve(ec1)
    return yin
    
print(calculo_yin(yin))


ec2 = Eq(Ec,yin+((q1**2)/(2*g*yin**2)))

yin = solve(ec2)

#print(round(yin[0],4))
#print(round(yin[1],4))
#print(round(yin[2],4))

print(Ec, yc)

EqCri = Eq(m,(0-yc)/(0-Ec))

m = solve(EqCri)

print(m)



yin = yin[2]

def grafica4 (qg1,qg2):

    x = np.linspace(0,10,50)

    yg = np.linspace(0.1,10,1000)
    yg2 = np.linspace(0.4,10,1000)
    
    E = yg + (qg1)**2/(2*g*yg**2) 
    E2 = yg2 + (qg2)**2/(2*g*yg2**2)
    

    plt.style.use('ggplot')
    plt.plot(E,yg,label = 'S1')
    plt.plot(E2,yg,label = 'S2')
    plt.plot(x,m*x,label = 'Ec = 3/2 yc')
    plt.plot(x,x)
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend()
    plt.show()

grafica4(q1,q2)














