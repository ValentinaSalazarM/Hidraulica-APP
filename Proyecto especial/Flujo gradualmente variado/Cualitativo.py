# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 22:57:20 2021

@author: JFGJ
"""
from PIL import Image
import numpy as np
import sympy as sp
from sympy import *

ys= symbols('ys')

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
        
        temp = 1/np.tan((np.pi/180)*propiedad)
    
        
    elif unidad == 'radianes':
        
        temp = 1/np.tan(propiedad)
    
    elif unidad == 'm':
    
       temp = propiedad
    else:
        temp = 'Error'
        
    return temp



def Area(y,b,m1,m2,uni,uni2):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (float) Pendiente parte derecha de un trapecio
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
            
    else:
        
        if m1 == m2:
                
            A = (b+m1*y)*y
                
        else:
                
            A = m1*y**2/2+b*y+m2*y**2/2 
            
    return A

print(Area(ys, 0, 50, 0, 'm', 'grados'))

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

print(Perimetro(ys, 0, 50, 0, 'm', 'grados'))

def T(y,b,m1,m2,uni,uni2):
    
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

    if b == 0:
        
        T = 2*y*m1

    if b!= 0 and m1 != 0 and m2 != 0:
        
        
        if m1 == m2:
                
            T = b + 2 * (m1*y)
                
        else:
                
            T = b + (m1*y) + (m2*y)

    return T

def yc(Q,g,y,b,m1,m2,uni,uni2):
    
    centinela = False
    
    i = 0
    
    ecu = Eq(1, Q**2*T(ys,b,m1,m2,uni,uni2)/(Area(ys, b, m1, m2, uni, uni2)**3*g))
    
    yc = solve(ecu)
    
    if b!= 0 and m1 != 0 and m2 != 0:
        
        yc = yc[1]
        
    else:
        
        yc = yc[0]
        
    return yc
    

def yn (n,Q,S,y,b,m1,m2,uni,uni2):
    
    temp = n*Q/sqrt(S)
    
    temp2 = Eq(temp, Area(ys,b,m1,m2,uni,uni2)**(5/3)/Perimetro(ys,b,m1,m2,uni,uni2)**(2/3))
    
    if S == 0:
        
        yn = 'Infinito'
        
    elif S < 0:
        
        yn = 'No existe'
        
    else:
        
        if b!= 0 and m1 != 0 and m2 != 0:
            
            yn = float(solve(temp2)[0])
            
        else:
       
            yn = solve(temp2)[0]
                   
    return yn

def TipoSeccion(n,Q,S,g,y,b,m1,m2,uni,uni2):
    
    yc1 = yc(Q,g,y,b,m1,m2,uni,uni2)
    yn1 = yn (n,Q,S,y,b,m1,m2,uni,uni2)
    
    if S == 0:
    
        msg = 'Horizontal'    
    
    elif S < 0:
        
        msg = 'Adversa'
    
    elif  yn1>yc1:
    
        msg = 'Suave'
        
    elif yc1>yn1:
        
        msg = 'Empinada'
    
    elif yc1 == yn1:
        
        msg = 'Critica'
        
    
        
    return msg


def abrir_imagen(im):
    
    ruta ='D:/Documents/Hidraulica-APP/Proyecto especial/Flujo gradualmente variado/' + im + '.jpeg'
    im = Image.open(ruta)
    im.show()

def tipoZona (yin, n, Q, S, g, y, b, m1, m2, uni, uni2):
    
    yc1 = yc(Q,g,y,b,m1,m2,uni,uni2)
    yn1 = yn (n,Q,S,y,b,m1,m2,uni,uni2)    
    msg = TipoSeccion(n, Q, S, g, y, b, m1, m2, uni, uni2)
        
    
    if msg == 'Suave':
    
        if yin > yn1:
            
            abrir_imagen('M1')
            
        elif yin < yn1 and yin > yc1:
        
            abrir_imagen('M2')
        
        elif yin < yc1:
        
            abrir_imagen('M3')
            
    elif msg == 'Empinada':
            
        if yin > yc1:
            
            abrir_imagen('S1')
            
        elif yin < yc1 and yin > yn1:
        
            abrir_imagen('S2')
        
        elif yin < yn1:
        
            abrir_imagen('S3')

    elif msg == 'Critica':

        if yin > yn1:
            
            abrir_imagen('C1')
            
        elif yin == yn1:
        
            abrir_imagen('C2')
        
        elif yin < yn1:
        
            abrir_imagen('C3')
    
    elif msg == 'Horizontal':
    
        
        if yin > yc1:
        
            abrir_imagen('H2')
        
        elif yin < yc1:
        
            abrir_imagen('H3')  

    if msg == 'Adversa':

                   
        if yin > yc1:
        
            abrir_imagen('A2')
        
        elif yin < yc1:
        
            abrir_imagen('A3')
            
    return msg



print('yc ,',yc(74.3, 9.81, ys, 8.3, 50, 50, 'm', 'grados'))
print('yn ,',yn(0.013, 74.3, 0.001, ys, 8.3, 50, 50, 'm', 'grados'))

yin = 2
print('yin ,',yin)

tipoZona(yin, 0.013, 74.3, 0.001, 9.81, ys, 8.3, 50, 50, 'm', 'grados')

















































