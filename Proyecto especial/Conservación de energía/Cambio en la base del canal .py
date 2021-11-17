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

##Desarrollo para cambio en la base del canal, parámetros b,y1,v1,z1,z2
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
            
    if b!= 0 and m1 != 0 and m2 != 0:
        
        
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
    

def Qfun(y,b,m1,m2,uni,uni2):
    
    """ Esta función retorna el caudal según la sección transversal\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: El cuadal de la sección transversal [m^3/s]
    """
    
    Q = v1 * Area(y,b,m1,m2,uni,uni2) 
    
    return Q


def y2fun(y1,y2,v1,b1,b2,m1,m2,g,uni,uni2):
    
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
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    y1 = cambio_unidades(uni,y1)
    b1 = cambio_unidades(uni,b1)
    b2 = cambio_unidades(uni,b2)
    m1 = cambio_angulo(uni2,m1)
    m2 = cambio_angulo(uni2,m2)
    Q = Qfun(y1,b1,m1,m2,uni,uni2)
    
    if m1 == 0 and m2 == 0:
        
        ec1 = Eq(y1+((v1**2)/(2*g)),y2+((Q**2)/(2*g*(b2*y2)**2)))
    
        y2 = solve(ec1)  
    
    if b!= 0 and m1 != 0 and m2 != 0:
        
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



def calculo_yc(yc,y1,b1,b2,m1,m2,g,uni,uni2):
    
    """ Esta función retorna la altura crítica del agua\n
        
    Parámetros:
        yc (symbol) variable que se quiere calcular
        y1 (float) altura del agua de la sección 1
        b1 (float) base del canal en la sección 1
        b2 (float) base del canal en la sección 2
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: La altura crítica del agua [m]
    """
    
    Q = Qfun(y1,b1,m1,m2,uni,uni2)
    ec1 = Eq(Q/sqrt(g),(Area(yc, b2, m1, m2,uni,uni2)*sqrt(Area(yc, b2, m1, m2,uni,uni2)))/sqrt(Tfun(yc, b2, m1, m2,uni,uni2)))
            
    yc = solve(ec1)[0]
    
    return yc



def calculo_v2(y1,y2,v1,b1,b2,m1,m2,g,uni,uni2):
    
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
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: La velocidad del agua en la sección 2 [m]
    """
    
    if y2fun(y1,y2,v1,b1,b2,m1,m2,g,uni,uni2) == "Fenomeno de choque, se requiere calcular yc\n":
        ecu = Eq(Qfun(y1,b1,m1,m2,uni,uni2),v2*Area(calculo_yc(yc,y1,b1,b2,m1,m2,g,uni,uni2),b2,m1,m2,uni,uni2))
        v = solve(ecu)
    else:
        if m1 == 0 and m2 == 0:
            
            ecu = Eq(Qfun(y1,b1,m1,m2,uni,uni2),v2*Area(y2fun(y1,y2,v1,b1,b2,m1,m2,g,uni,uni2)[2],b2,m1,m2,uni,uni2))
            v = solve(ecu)
            
        if b!= 0 and m1 != 0 and m2 != 0:
            ecu = Eq(Qfun(y1,b1,m1,m2,uni,uni2),v2*Area(max(y2fun(y1,y2,v1,b1,b2,m1,m2,g,uni,uni2)),b2,m1,m2,uni,uni2))
            v = solve(ecu)
    
    return v


def calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g,uni,uni2):

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
        uni Unidades propiedades (mm,cm,m,in)
        uni2 Unidades angulo (grados,radianes,m)
    Retorna:
        float: La velocidad del agua en la sección 2 [m]
    """
    
    ecu = Eq(Ec,calculo_yc(yc,y1,b1,b2,m1,m2,g,uni,uni2) + calculo_v2(y1,y2,v1,b1,b2,m1,m2,g,uni,uni2)[0]**2/(2*g))
    
    Ec = solve(ecu)
    
    return Ec

def calculo_yin(Ec,yin,y1,y2,v1,b1,b2,m1,m2,g,uni,uni2):
    
    Q = Qfun(y1,b1,m1,m2,uni,uni2)
    Ec = calculo_Ec(Ec,yin,y1,y2,v1,b1,b2,m1,m2,g,uni,uni2)[0]

    if m1 == 0 and m2 == 0:
        
        ec1 = Eq(Ec,yin+((Q**2)/(2*g*(b1*yin)**2)))
    
        yin = solve(ec1)  
    
    if b == 0 and m1 != 0 and m2 != 0:
        
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


def grafica4 (Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uni,uni2):

    Q = Qfun(y1,b1,m1,m2,uni,uni2)
    EqCri = Eq(m,(0-calculo_yc(yc,y1,b1,b2,m1,m2,g,uni,uni2))/(0-calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g,uni,uni2)[0]))
    m = solve(EqCri)

    x = np.linspace(0,10,50)

    yg = np.linspace(0.1,10,1000)
    yg2 = np.linspace(0.4,10,1000)
    
    E = yg + (Q**2/(2*g*(Area(yg,b1,m1,m2,uni,uni2))**2))
    E2 = yg + (Q**2/(2*g*(Area(yg,b2,m1,m2,uni,uni2))**2))
    

    plt.style.use('ggplot')
    plt.plot(E,yg,label = 'S1')
    plt.plot(E2,yg,label = 'S2')
    plt.plot(x,x, label = 'E = y',linestyle='dashed')
    if m1 != 0 and m2 != 0:
        plt.plot(x,m*x,label = 'Ec = 3/2 yc', linestyle='dashed')
        
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend()
    plt.show()


def imprimir_valores(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uni,uni2):
    
    msg1 = '\nArea1 '+ str( Area(y1,b1,m1,m2,'m',''))
    
    msg2 = '\nCaudal '+ str(Qfun(y1,b1,m1,m2,'m',''))
    
    msg3 = '\nvalores de y2 '+ str(y2fun(y1,y2,v1,b1,b2,m1,m2,g,'m',''))
    
    msg4 = '\nvalor de yc'+ str(calculo_yc(yc,y1,b1,b2,m1,m2,g,'m',''))
    
    msg5 = '\nvalor de Ec'+ str(calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g,'m',''))

    msg6 = '\nvelocidad en 2 '+ str(calculo_v2(y1,y2,v1,b1,b2,m1,m2,g,'m',''))   
    
    msg7= '\nNuevo y1 '+ str( max(calculo_yin(Ec,yin,y1,y2,v1,b1,b2,m1,m2,g,'m','')))
   
    grafica4(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,'m','')
    
    return msg1 + msg2 + msg3+ msg4+ msg5+ msg6+ msg7
    
print(imprimir_valores(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,'m',''))













