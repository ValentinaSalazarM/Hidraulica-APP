# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 22:57:20 2021

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
        
        temp = 1/np.tan((np.pi/180)*propiedad)
    
        
    elif unidad == 'radianes':
        
        temp = 1/np.tan(propiedad)
    
    else:
       temp = propiedad
        
    return temp

def cambio_caudal(unidad,propiedad):
    
    """ Esta realiza el cambio de unidades de caudal\n        
    Parámetros:
        unidad (string) Puede ser L/s o m3/s. 
        propiedad (float) Valor del caudal.
    Retorna:
        float: Retorna el caudal en m3/s.
    """
    
    if unidad == 'L':
        
        temp = propiedad/1000
    else:
        temp = propiedad
        
    return temp

def Area(y,b,m1,m2,uniy,unib,unim1,unim2):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (float) Pendiente parte derecha de un trapecio
        uniy Unidades propiedades (mm,cm,m,in)
        unib Unidades propiedades (mm,cm,m,in)
        unim1 Unidades angulo (grados,radianes,m)
        unim2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: El área de la sección transversal [m^2]
    """
    
    y = cambio_unidades(uniy,y)
    b = cambio_unidades(unib,b)
    m1 = cambio_angulo(unim1,m1)
    m2 = cambio_angulo(unim2,m2)
    
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



def Perimetro(y,b,m1,m2,uniy,unib,unim1,unim2):
    """ Esta función retorna el perimetro de la sección transversal\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uniy Unidades propiedades (mm,cm,m,in)
        unib Unidades propiedades (mm,cm,m,in)
        unim1 Unidades angulo (grados,radianes,m)
        unim2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: El espejo de agua de la sección transversal [m]
    """
    y = cambio_unidades(uniy,y)
    b = cambio_unidades(unib,b)
    m1 = cambio_angulo(unim1,m1)
    m2 = cambio_angulo(unim2,m2)

    if m1 == 0 and m2 == 0:
        
        P = b+2*y

    elif b==0:
        
        P = 2*y*(1+m1**2)**(1/2)
        
    elif b!= 0 and m1 != 0 and m2 != 0:
        
        if m1 == m2:
                
            P = b + 2*y*(1+m1**2)**(1/2)
                
        else:
                
            P = b + y*(1+m1**2)**(1/2)+y*(1+m2**2)**(1/2)
    
    return P


def T(y,b,m1,m2,uniy,unib,unim1,unim2):
    
    """ Esta función retorna el espejo de agua según la sección transversal\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uniy Unidades propiedades (mm,cm,m,in)
        unib Unidades propiedades (mm,cm,m,in)
        unim1 Unidades angulo (grados,radianes,m)
        unim2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: El espejo de agua de la sección transversal [m]
    """

    y = cambio_unidades(uniy,y)
    b = cambio_unidades(unib,b)
    m1 = cambio_angulo(unim1,m1)
    m2 = cambio_angulo(unim2,m2)

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

def yc(Q,g,b,m1,m2,unib,uniy,unim1,unim2,uniQ):
    
    """ Esta función retorna la altura crítica \n
        
    Parámetros:
        Q (float) caudal
        g (float) velocidad gravitacional
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uniy Unidades propiedades (mm,cm,m,in)
        unib Unidades propiedades (mm,cm,m,in)
        unim1 Unidades angulo (grados,radianes,m)
        unim2 Unidades angulo (grados,radianes,m)
        uniQ Unidades del caudal (m3/s, L/s)
    Retorna:
        float: El espejo de agua de la sección transversal [m]
    """
    
    ys= symbols('ys')
    
    Q = cambio_caudal(uniQ, Q)
    
    ecu = Eq(1, Q**2*T(ys,b,m1,m2,uniy,unib,unim1,unim2)/(Area(ys, b, m1, m2, uniy, unib,unim1,unim2)**3*g))
    
    yc = solve(ecu)
    
    if b!= 0 and m1 != 0 and m2 != 0:
        
        yc = yc[1]
        
    else:
        
        yc = yc[0]
        
    return yc
    

def yn (n,Q,S,b,m1,m2,unib,uniy,unim1,unim2,uniQ,uniS):
    
    """ Esta función retorna la altura normal \n
        
    Parámetros:
        n (float) n de Manning
        Q (float) caudal
        S (float) pendiente del canal
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uniy Unidades propiedades (mm,cm,m,in)
        unib Unidades propiedades (mm,cm,m,in)
        unim1 Unidades angulo (grados,radianes,m)
        unim2 Unidades angulo (grados,radianes,m)
        uniQ Unidades del caudal (m3/s, L/s)
        uniS Unidades angulo (grados,radianes,m)
    Retorna:
        float: El espejo de agua de la sección transversal [m]
    """
    ys= symbols('ys')
    Q = cambio_caudal(uniQ, Q)
    S = cambio_angulo(uniS,S)
    
    temp = n*Q/S**(1/2)

    A = Area(ys, b, m1, m2, uniy, unib, unim1, unim2)
    P = Perimetro(ys, b, m1, m2, uniy, unib, unim1, unim2)

    
    temp2 = Eq(temp, A**(5/3)/P**(2/3))
    

    if S == 0:
        
        yn = 'Infinito'
        
    elif S < 0:
        
        yn = 'No existe'
        
    else:
        
        if b!= 0 and m1 != 0 and m2 != 0:
            
            yn = float(solve(temp2)[0])
            
        else:
       
            yn = float(solve(temp2)[0])

    return yn

def TipoSeccion(n,Q,S,g,b,m1,m2,unib,uniy,unim1,unim2,uniQ,uniS):
    
    """ Esta función retorna la altura normal \n
        
    Parámetros:
        n (float) n de Manning
        Q (float) caudal
        S (float) pendiente del canal
        g (float) velocidad gravitacional
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uniy Unidades propiedades (mm,cm,m,in)
        unib Unidades propiedades (mm,cm,m,in)
        unim1 Unidades angulo (grados,radianes,m)
        unim2 Unidades angulo (grados,radianes,m)
        uniQ Unidades del caudal (m3/s, L/s)
        uniS Unidades angulo (grados,radianes,m)
    Retorna:
        float: El espejo de agua de la sección transversal [m]
    """
    S = cambio_angulo(uniS,S)
    yc1 = yc(Q,g,b,m1,m2,unib,uniy,unim1,unim2,uniQ)
    yn1 = yn (n,Q,S,b,m1,m2,unib,uniy,unim1,unim2,uniQ,uniS)
    
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


def tipoZona (yin, n, Q, S, g, b, m1, m2, unib, uniy, unim1,unim2,uniQ,uniS):
    
    
    yc1 = yc(Q,g,b,m1,m2,unib,uniy,unim1,unim2,uniQ)
    yn1 = yn (n,Q,S,b,m1,m2,unib,uniy,unim1,unim2,uniQ,uniS)
    msg = TipoSeccion(n,Q,S,g,b,m1,m2,unib,uniy,unim1,unim2,uniQ,uniS)
    nombre_imagen = ''
    
    if msg == 'Suave':
    
        if yin > yn1:
            
            nombre_imagen = 'M1'
            
        elif yin < yn1 and yin > yc1:
        
            nombre_imagen = 'M2'
        
        elif yin < yc1:
        
            nombre_imagen = 'M3'
            
    elif msg == 'Empinada':
            
        if yin > yc1:
            
            nombre_imagen = 'S1'
            
        elif yin < yc1 and yin > yn1:
        
            nombre_imagen = 'S2'
        
        elif yin < yn1:
            nombre_imagen = 'S3'

    elif msg == 'Critica':

        if yin > yn1:
            
            nombre_imagen = 'C1'
            
        elif yin == yn1:
        
            nombre_imagen = 'C2'
        
        elif yin < yn1:
            
            nombre_imagen = 'C3'
    
    elif msg == 'Horizontal':
    
        if yin > yc1:
        
            nombre_imagen = 'H2'
        
        elif yin < yc1:
        
            nombre_imagen = 'H3'  

    if msg == 'Adversa':

                   
        if yin > yc1:
            
            nombre_imagen = 'A2'
        
        elif yin < yc1:
        
            nombre_imagen = 'A3'
            
    return msg, nombre_imagen

def pendiente_critica(n, Q, S, g, b, m1, m2, unib, uniy, unim1,unim2,uniQ):
    
    """ Calcula la pendiente crítica con en n de manning\n
        
    Parámetros:
        d (float) diametro.
        n (float) n de Manning    
        g (float) aceleración gravitacional, usualmente 9.81
        Ryd (float) Porcentaje de la relación y/d. 
        unid Unidades del diametro de la tubería (mm,cm,m,in)
    Retorna:
        float: pendiente crítica
    """
    
    Sct = symbols('Sct')
    
    yc1 = yc(Q,g,b,m1,m2,unib,uniy,unim1,unim2,uniQ)
    temp = n*Q/Sct**(1/2)

    A = Area(yc1, b, m1, m2, uniy, unib, unim1, unim2)
    P = Perimetro(yc1, b, m1, m2, uniy, unib, unim1, unim2)

    
    temp2 = Eq(temp, A**(5/3)/P**(2/3))
    
    Sc = solve(temp2)
    
    return Sc

def valores (yin, n, Q, S, g, b, m1, m2, unib, uniy, unim1,unim2,uniQ,uniS):
    
    yc1 = yc(Q,g,b,m1,m2,unib,uniy,unim1,unim2,uniQ)
    yn1 = yn (n,Q,S,b,m1,m2,unib,uniy,unim1,unim2,uniQ,uniS) 
    Sc = pendiente_critica(n, Q, S, g, b, m1, m2, unib, uniy, unim1, unim2, uniQ)
        
    return yc1, yn1, Sc, tipoZona(yin, n, Q, S, g, b, m1, m2, unib, uniy, unim1,unim2,uniQ,uniS)

yin = 1
print('yin ,',yin)
n = 0.013
Q = 74.3
S = 0.01
g = 9.81
b = 8.3
m1 = 50
m2 = 50
unib = 'm'
uniy = 'm'
unim1 = 'm'
unim2 = 'm'
uniQ = 'm'
uniS = 'm'
print(pendiente_critica(n, Q, S, g, b, m1, m2, unib, uniy, unim1, unim2, uniQ))
print(valores(yin, n, Q, S, g, b, m1, m2, unib, uniy, unim1,unim2,uniQ,uniS))

















































