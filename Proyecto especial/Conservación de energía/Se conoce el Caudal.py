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


'Variables para la solución del problema'



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

def Area(y,b,m1,m2,uniy,unib,unim):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (float) Pendiente parte derecha de un trapecio
        unib Unidades de la base propiedades (mm,cm,m,in)
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: El área de la sección transversal [m^2]
    """
    
    y = cambio_unidades(uniy,y)
    b = cambio_unidades(unib,b)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    
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

def calculo_dz(z1,z2,uniz1,uniz2):
    
    """ Esta función retorna el valor de deltaz\n
    Parametros:
        z1 (float) Altura del fondo del canal en la sección 1  
        z2 (float) Altura del fondo del canal en la sección 2
        uniz1 Unidades de la altura del fondo del canal seccion 1 propiedades (mm,cm,m,in)
        uniz2 Unidades de la altura del fondo del canal seccion 2 propiedades (mm,cm,m,in)
    Retorna:
        float: La diferencia de alturas del fondo del canal[m]
    """
    
    z1 = cambio_unidades(uniz1,z1)
    z2 = cambio_unidades(uniz2,z2)
    
    return abs(z1-z2)
    
def calculo_y1(Q,v1,b,m1,m2,uniQ,unib,unim):
    
    """ Esta función retorna el valor de y1\n
        
    Parámetros:
        Q (float) Caudal del canal [m3/s]
        v1 (float) Velocidad de la sección 1
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (int) Pendiente parte derecha de un trapecio
        uniQ Unidades del cuadal (m3,L)
        unib Unidades de la base (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: La altura del agua en la seccion 1 [m]
    """
    y1 = symbols('y1')
    Q = cambio_caudal(uniQ,Q)
    b = cambio_unidades(unib,b)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    
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


def Q_en_litros(Q,uniQ):
    
    """ Esta función retorna el caudal en L/s \n

    Parámetros:
        Q (float) Caudal en m^3/s
        uniQ Unidades del cuadal (m3,L)
    Retorna:
        float: El cuadal de la sección transversal [L/s]
    """
    
    if uniQ == 'L':
        QL = Q
    else:
        QL = Q *1000
        
    return QL



def y2fun(Q,v1,b,m1,m2,z1,z2,g,uniQ,unib,unim,uniz1,uniz2):
    
    """ Esta función retorna la altura del agua en la sección dos\n
        
    Parámetros:
        Q (float) Caudal del canal
        v1 (float) Velocidad de la sección 1
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (float) Pendiente parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
        uniQ Unidades del cuadal (m3,L)
        unib Unidades de la base (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
        uniz1 Unidades de la altura del fondo del canal seccion 1 propiedades (mm,cm,m,in)
        uniz2 Unidades de la altura del fondo del canal seccion 2 propiedades (mm,cm,m,in)
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    y2 = symbols('y2')
    Q = cambio_caudal(uniQ,Q)
    b = cambio_unidades(unib,b)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    y1 = calculo_y1(Q,v1,b,m1,m2,uniQ,unib,unim)
    dz = calculo_dz(z1,z2,uniz1,uniz2)
    
    
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


def y2_final_valor(b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2):
    
    """ Esta función retorna la altura del agua en la sección dos\n    
    Parámetros:
        b (float) base del canal
        y1 (float) altura del agua en la sección 1
        m1 (float) Pendiente parte izquierda de un trapecio
        m2 (float) Pendiente parte derecha de un trapecio
        v1 (float) velocidad de la sección 1 del canal
        z1 (float) Altura del fondo del canal en la sección 1  
        z2 (float) Altura del fondo del canal en la sección 2
        g (float) Aceleración gravitacional, generalmente 9.81 
        unib Unidades de la base propiedades (mm,cm,m,in)
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
        uniz1 Unidades de la altura del fondo del canal seccion 1 propiedades (mm,cm,m,in)
        uniz2 Unidades de la altura del fondo del canal seccion 2 propiedades (mm,cm,m,in)
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    yf = y2fun(Q,v1,b,m1,m2,z1,z2,g,uniQ,unib,unim,uniz1,uniz2)
    temp = ''
    i=0
    y =[]
    
    while i<len(yf):
        
        y.append(round(yf[i],3))
        i+=1
    
    if b!=0 and m1 !=0 and m2 != 0:
        temp = round(max(yf),2)
    else:
        temp = y[2]
    
    return temp

def grafica3 (Q,b,m1,m2,uniQ,unib,unim,uniz1,uniz2):

    """ Esta función grafica la gráfica de enerigía específica \n
        según la sección transversal
    Parametros:
        Q (float) Caudal.
        b (float) base del canal
        m1 (int) Pendiente del lado izquierdo o pendientre triangular del canal 
        m2 (float) Pendiente parte derecha de un trapecio
        uniQ Unidades del cuadal (m3,L)
        unib Unidades de la base (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
        uniz1 Unidades de la altura del fondo del canal seccion 1 propiedades (mm,cm,m,in)
        uniz2 Unidades de la altura del fondo del canal seccion 2 propiedades (mm,cm,m,in)
    Retorna:
        plot: Gráfica de energía específica[m]
    """
    
    Q = cambio_caudal(uniQ,Q)
    b = cambio_unidades(unib,b)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)

    x = np.linspace(0,10,10)

    yg = np.linspace(0.2,10,300)     
    
    A = Area(yg,b,m1,m2,uniy,unib,unim)
    
    Ei = yg + (Q**2/(2*g*(A)**2))

    plt.style.use('classic')
    plt.plot(Ei,yg,label = 'S8')
    plt.plot(x,x, label = 'E = y', linestyle='dashed')
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend(loc='upper left')
    plt.show()

def grafica3_txt (Q,v1,b,m1,m2,z1,z2,g,uniQ,unib,unim,uniz1,uniz2,ruta):

    """ Esta función retorna un txt para graficar la enerigía específica \n
        según la sección transversal
    Parametros:
        v1 (float) velocidad de la sección 1 del canal
        b (float) base del canal
        y1 (float) altura del agua
        m1 (float) Pendiente parte izquierda de un trapecio
        m2 (float) Pendiente parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
        unib Unidades de la base propiedades (mm,cm,m,in)
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        txt: valores de x y y para graficar
    """
    
    x = np.linspace(0,10,10)
    yg = np.linspace(0.2,10,300) 
    Q = Q
    
    file = open(ruta, 'w')
   
    for index in range(len(yg)):
        
        A = Area(yg[index],b,m1,m2,uniy,unib,unim)
        
        Ei = yg[index] + (Q)**2/(2*g*(A)**2)  
        
        file.write(str(yg[index]) + ";" + str(Ei) + "\n")
        
    file.write("Linea Recta\n")
    
    for index in range(len(x)):
        
        file.write(str(x[index]) + ";" + str(x[index]) + "\n")
        
    file.close()

def imprimir_valores(Q, v1, b, m1, m2, z1, z2, g, uniQ, unib, unim, uniz1, uniz2):
    
    """ Esta función retirna los valores del caudal, el área y la gráfica
    Retorna:
        plot: Gráfica de energía específica
        str: Mensaje con los valores de caudal y área
    """
    
    yf = y2fun(Q,v1,b,m1,m2,z1,z2,g,uniQ,unib,unim,uniz1,uniz2)
    grafica3(Q,b,m1,m2,uniQ,unib,unim,uniz1,uniz2)
    i=0
    y =[]
    
    while i<len(yf):
        
        y.append(str(round(yf[i],3)) + ' [m]')
        i+=1
        
    msg1 = '\nLa altura inicial del agua (y1) es: '+str(calculo_y1(Q,v1,b,m1,m2,uniQ,unib,unim))+' [m]'
    msg2 = '\nEl cuada es:'+str(round(Q_en_litros(Q,uniQ),4))+ ' [l/s]'
    msg3 = '\nLos valores de y2 son: '+ str(y)
    msg4 = '\nEl valor final de y2 es: '+ str(y2_final_valor(b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2))
    msg5 = '\nEl valor de delta z es: '+str(round(calculo_dz(z1,z2,uniz1,uniz2),2))+' [m]'
    
    msg = msg1 + msg2 +msg3 +msg4 +msg5
    
    return msg 

def valores(Q,v1,b,m1,m2,z1,z2,g,uniQ,unib,unim,uniz1,uniz2):
    
    temp = ''
    Q = cambio_caudal(uniQ,Q)
    b = cambio_unidades(unib,b)
    z1 = cambio_unidades(uniz1,z1)
    z2 = cambio_unidades(uniz2,z2)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    
    y_1 = calculo_y1(Q, v1, b, m1, m2, uniQ, unib, unim)
    
    A1 = Area(y_1,b,m1,m2,uniy,unib,unim)
    
    Q = Q
    
    QL = Q_en_litros(Q,uniQ)
    
    y_2 = y2fun(Q,v1,b,m1,m2,z1,z2,g,uniQ,unib,unim,uniz1,uniz2)
    
    y_2_final = y2_final_valor(b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2)
    
    A2 = Area(b,y_2_final,m1,m2,unib,uniy,unim)
    
    print(y_1,A1, Q, QL, y_2,y_2_final,A2)
    
    return temp

uniQ = "m3"
unib = 'm'
uniy = 'm'
uniz1 = 'm'
uniz2 = 'm'
unim = ''
ruta = 'D:\Documents\Hidraulica-APP\Proyecto especial\Conservación de energía/seconocecaudal.cvs'

Q=55
b=5
v1=1.25
z1=0.2
z2=0
m1=0
m2=0
g=9.81

print(imprimir_valores(Q, v1, b, m1, m2, z1, z2, g, uniQ, unib, unim, uniz1, uniz2))
print(valores(Q, v1, b, m1, m2, z1, z2, g, uniQ, unib, unim, uniz1, uniz2))
print(grafica3_txt (Q, v1, b, m1, m2, z1, z2, g, uniQ, unib, unim, uniz1, uniz2, ruta))































