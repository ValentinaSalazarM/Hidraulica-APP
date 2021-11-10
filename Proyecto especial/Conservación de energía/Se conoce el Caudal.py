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

y1,y2 = symbols('y1 y2')

##Desarrollo con caudal conocido, parámetros b,Q,v1,z1,z2
'-----------------------------------------------------------------------------'
'-----------------------------------------------------------------------------'

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

def calculo_dz(z1,z2,uni):
    
    """ Esta función retorna el valor de deltaz\n
    Parametros:
        z1 (float) Altura del fondo del canal en la sección 1  
        z2 (float) Altura del fondo del canal en la sección 2
        uni Unidades propiedades (mm,cm,m,in)
    Retorna:
        float: La diferencia de alturas del fondo del canal[m]
    """
    
    z1 = cambio_unidades(uni,z1)
    z2 = cambio_unidades(uni,z2)
    
    return abs(z1-z2)
    
def calculo_y1(y1,Q,v1,b,m1,m2,uni,uni2):
    
    """ Esta función retorna el valor de y1\n
        
    Parámetros:
        y1 (symbol) variable que se quiere calcular
        Q (float) Caudal del canal [m3/s]
        v1 (float) Velocidad de la sección 1
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (int) Pendiente parte derecha de un trapecio
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: La altura del agua en la seccion 1 [m]
    """
    
    b = cambio_unidades(uni,b)
    m1 = cambio_angulo(uni2,m1)
    m2 = cambio_angulo(uni2,m2)
    
    if m1 == 0 and m2 == 0:
        
        ecu = Eq(Q,v1*(b * y1))
        
        y1 = solve(ecu)
        
        return round(y1[0],2)

    elif b == 0:
        
        ecu = Eq(Q,v1*y1**2 * m1)
            
        y1 = solve(ecu)
            
        return round(y1[1],2)
            
    else:
        
        if m1 == m2:
                
            ecu = Eq(Q,v1*((b+m1*y1)*y1))
                
            y1 = solve(ecu)
                
            return round(y1[1],2)
                
        else:
                
            ecu = Eq(Q,v1*(m1*y1**2/2+b*y1+m2*y1**2/2))
                
            y1 = solve(ecu)
                
            return round(y1[1],2)
    return "Error en y1"


def Q_en_litros(Q):
    
    """ Esta función retorna el caudal en L/s \n

    Parámetros:
        Q (float) Caudal en m^3/s
    Retorna:
        float: El cuadal de la sección transversal [L/s]
    """
    
    QL = Q *1000
    return QL



def y2fun(y1,y2,Q,v1,b,m1,m2,z1,z2,g,uni,uni2):
    
    """ Esta función retorna la altura del agua en la sección dos\n
        
    Parámetros:
        y1 (symbol) variable que se quiere calcular
        y2 (symbol) variable que se quiere calcular
        Q (float) Caudal del canal
        v1 (float) Velocidad de la sección 1
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (float) Pendiente parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    b = cambio_unidades(uni,b)
    m1 = cambio_angulo(uni2,m1)
    m2 = cambio_angulo(uni2,m2)
    y1 = calculo_y1(y1,Q,v1,b,m1,m2,uni,uni2)
    dz = calculo_dz(z1,z2,uni)
    
    
    if m1 == 0 and m2 == 0:
        
        ec1 = Eq(y1+((v1**2)/(2*g))+dz,y2+((Q**2)/(2*g*(b*y2)**2)))
    
        y2 = solve(ec1)
    
    elif b == 0:
        
        ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Q**2)/(2*g*(y2**2*m1)**2))+z2)
    
        y2 = solve(ec1)       
    
    else:
        
        if m1 == m2:
                
            ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Q**2)/(2*g*((b+m1*y2)*y2)**2))+z2)
    
            y2 = solve(ec1)
                
        else:
            ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Q**2)/(2*g*(m1*y2**2/2+b*y2+m2*y2**2/2)**2))+z2)
            
            y2 = solve(ec1)
    
    i=0
    y =[]
    
    while i<len(y2):
        
        y.append(round(y2[i],3))
        i+=1
    
    return y 


def grafica3 (b,m1,m2,uni,uni2):

    """ Esta función grafica la gráfica de enerigía específica \n
        según la sección transversal
    Parametros:
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (float) Pendiente parte derecha de un trapecio
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        plot: Gráfica de energía específica[m]
    """

    b = cambio_unidades(uni,b)
    m1 = cambio_angulo(uni2,m1)
    m2 = cambio_angulo(uni2,m2)


    x = np.linspace(0,10,10)

    yg = np.linspace(0.2,10,300) 
    
    Ei = yg + (Q**2/(2*g*(Area(yg,b,m1,m2,uni,uni2))**2))

    plt.style.use('classic')
    plt.plot(Ei,yg,label = 'S8')
    plt.plot(x,x, label = 'E = y', linestyle='dashed')
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend(loc='upper left')
    plt.show()

def imprimir_valores():
    
    """ Esta función retirna los valores del caudal, el área y la gráfica
    Retorna:
        plot: Gráfica de energía específica
        str: Mensaje con los valores de caudal y área
    """
    
    b=10
    y1=4.5
    v1=1.25
    z1=0
    z2=1.05
    m1=0
    m2=0
    
    
    yf = y2fun(y1,y2,Q,v1,b,m1,m2,z1,z2,g,'m','')
    grafica3(b,m1,m2,'m','')
    i=0
    y =[]
    
    while i<len(yf):
        
        y.append(str(round(yf[i],3)) + ' [m]')
        i+=1
        
    msg1 = '\nLa altura inicial del agua (y1) es: '+str(calculo_y1(y1,Q,v1,b,m1,m2,'m',''))+' [m]'
    msg2 = '\nEl cuada es:'+str(round(Q_en_litros(Q),4))+ ' [l/s]'
    msg3 = '\nLos valores de y2 son: '+ str(y)
    
    if b!=0 and m1!=0 and m2 !=0:
        msg4 = '\nLa altura final del agua (y2) es: '+str(round(max(yf),2))
    else:
        msg4 = '\nLa altura final del agua (y2) es: '+str(y[2])
        
    msg5 = '\nEl valor de delta z es: '+str(round(calculo_dz(z1,z2,'m'),2))+' [m]'
    
    msg = msg1 + msg2 +msg3 +msg4 +msg5
    
    return msg 

print(imprimir_valores())
































