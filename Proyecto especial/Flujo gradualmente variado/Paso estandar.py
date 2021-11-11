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

y1,y2,y = symbols('y1 y2 y')

##Desarrollo método de paso estandar,
'-----------------------------------------------------------------------------'
'-----------------------------------------------------------------------------'
delta_x = 10
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


def Perimetro(y,b,m1,m2,uni,uni2):
    """ Esta función retorna el perimetro de la sección transversal\n
        
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
        
        P = b+2*y

    elif b==0:
        
        P = 2*y*sqrt(1+m1**2)
        
    elif b!= 0 and m1 != 0 and m2 != 0:
        
        if m1 == m2:
                
            P = b + 2*y*sqrt(1+m1**2)
                
        else:
                
            P = b + y*sqrt(1+m1**2)+y*sqrt(1+m2**2)
    
    return P


def Radio_Hidraulico(y,b,m1,m2,uni,uni2):
    """ Esta función retorna el radio hidraulico de la sección transversal\n
        
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
        
        R = b*y/(b+2*y)

    elif b==0:
        
        R = m1*y/(2*sqrt(1+m1**2))
        
    elif b!= 0 and m1 != 0 and m2 != 0:
        
        if m1 == m2:
                
            R = (b +m1*y)*y/(b+2*y*sqrt(1+m1**2))
                
        else:
            #REVISAR    
            R = (b +m1*y)*y/(b+y*sqrt(1+m1**2)+y*sqrt(1+m2**2))
    
    return R

def yc(Q,y,b,m1,m2,g,uni,uni2,uni3):
    
    """ Esta función retorna la altura crítica del agua\n
        
    Parámetros:
        Q (float) Caudal.
        y (symbol) variable que se quiere calcular
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
    ec1 = Eq(Q/sqrt(g),(Area(y, b, m1, m2,uni,uni2)*sqrt(Area(y, b, m1, m2,uni,uni2)))/sqrt(Tfun(y, b, m1, m2,uni,uni2)))
            
    yc = solve(ec1)[0]
    
    return yc

def yn(Q,n,So,y, b, m1, m2, uni, uni2):
    ''' Calcula la altura normal de la sección \n
    Parametros:
        Q (float) Caudal.
        n (float) n de manning.
        So (float) pendiente del fondo del canal.
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: Altura crítica del agua.
    '''
    Q = cambio_unidades_Caudal(uni2,Q)
    
    ecu = Eq((n*Q)/sqrt(So),(Area(y, b, m1, m2, uni, uni2)**(5/3))/(Perimetro(y, b, m1, m2, uni, uni2)**(2/3)))
    
    yn = round(float(solve(ecu)[0]),3)
    
    return yn

def ciclo(delta_x,Q,n,So,L,y, b, m1, m2, g, uni, uni2, uni3):
    
    x = 0
    centinela = False
    
    #Primer paso
    y_temp = yc(Q, y, b, m1, m2, g, uni, uni2, uni3)
    print('y ',y_temp)
    A = Area(y_temp, b, m1, m2, uni, uni2)
    print('Area ',A)
    P = Perimetro(y_temp, b, m1, m2, uni, uni2)
    print('Perimetro ',P)
    R = A/P
    print('Radio ',R)
    v = Q/A
    print('Velocidad ',v)
    temp = v**2/(2*g)
    print('Cabeza de velocidad ',temp)
    E = temp + y_temp
    print('Energía ',E)
    z = x * So
    print('Fondo ',z)
    H1 = z+E
    print('H1 ',H1) 
    Sfi = n**2*Q**2/(A**2*R**(4/3))
    print('Sfi ',Sfi)
    
    while centinela == False:
        
        delta_x = delta_x+delta_x
        
        y_temp = y_temp+0.01
        print('y ',y_temp)
        
        A = Area(y, b, m1, m2, uni, uni2)
        #print('Area ',A)
        P = Perimetro(y, b, m1, m2, uni, uni2)
        #print('Perimetro ',P)
        R = A/P
        #print('Radio ',R)
        v = Q/A
        #print('Velocidad ',v)
        temp = v**2/(2*g)
        #print('Cabeza de velocidad ',temp)
        E = temp + y
        #print('Energía ',E)
        z = x * So
        #print('Fondo ',z)
        H1 = z+E
        #print('H1 ',H1) 
        Sf = n**2*Q**2/(A**2*R**(4/3))
        #print('Sf ',Sf)
        Sfm = (Sfi+Sf)/2
        #print('Sfm ',Sfm)
        Sfi = Sf
        #print('Sfi ',Sfi)
        H2 = H1+Sfm*delta_x
        #print('H2 ',H2)
        er = abs(H1-H2)
        print('Error',er)
        
        ecu1 = Eq(er,0)
        y = solve(ecu1)
        print(y)
        
        if delta_x>L:
            centinela = True
        
        
        
        
        
    
    
    

#print(Area(y, b2, m1, m2,'m','m',))
#print(yc(Q,y,b2,0,0,g,'m','m','m^3/s'))
#print(yn(Q,n2,So,y,b2,0,0,'m','m^3/s'))
print(ciclo(10,Q,n2,So,L2,y, b2, 0,0, g, 'm','m', 'm^3/s'))





















































