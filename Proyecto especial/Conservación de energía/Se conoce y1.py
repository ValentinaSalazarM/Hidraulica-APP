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

##Desarrollo para cuando se conoce y1, parámetros b,y1,v1,z1,z2
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

def Area(b,y,m1,m2,unib,uniy,unim):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        b (float) base del canal
        y (float) altura del agua
        m1 (float) Pendiente parte izquierda de un trapecio
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



def Qfun(v1,b,y,m1,m2,unib,uniy,unim):
    
    """ Esta función retorna el caudal según la sección transversal\n
        
    Parámetros:
        v1 (float) velocidad inicial
        b (float) base del canal
        y (float) altura del agua
        m1 (float) Pendiente parte izquierda de un trapecio
        m2 (float) Pendiente parte derecha de un trapecio
        unib Unidades de la base propiedades (mm,cm,m,in)
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: El cuadal de la sección transversal [m^3/s]
    """
    
    Q = v1 * Area(b,y,m1,m2,unib,uniy,unim) 
    
    return Q


def Q_en_litros(v1,b,y,m1,m2,unib,uniy,unim):
    
    """ Esta función retorna el caudal en L/s \n

    Parámetros:
        v1 (float) velocidad inicial
        b (float) base del canal
        y (float) altura del agua
        m1 (float) Pendiente parte izquierda de un trapecio
        m2 (float) Pendiente parte derecha de un trapecio
        unib Unidades de la base propiedades (mm,cm,m,in)
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: El cuadal de la sección transversal [L/s]
    """
    
    QL = Qfun(v1,b,y,m1,m2,unib,uniy,unim) *1000
    return QL



def y2fun(y2,b,y1,m1,m2,v1,z1,z2,g,unib,uniy,unim,uniz1,uniz2):
    
    """ Esta función retorna la altura del agua en la sección dos\n
        
    Parámetros:
        y2 (symbol) variable que se quiere calcular
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
        List: los valores de las alturas del agua en la sección 2 [m]
    """
    b = cambio_unidades(unib,b)
    y1 = cambio_unidades(uniy,y1)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    z1 = cambio_unidades(uniz1,z1)
    z2 = cambio_unidades(uniz2,z2)
    
    Q = Qfun(v1,b,y1,m1,m2,unib,uniy,unim)
    
    if m1 == 0 and m2 == 0:
        
        ec1 = Eq(y1+((v1**2)/(2*g))+z1,y2+((Q**2)/(2*g*(b*y2)**2))+z2)
    
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
    
    return y2 

def y2_final_valor(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2):
    
    """ Esta función retorna la altura del agua en la sección dos\n    
    Parámetros:
        y2 (symbol) variable que se quiere calcular
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
    yf = y2fun(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2)
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
    

def grafica2 (v1,b,y,m1,m2,g,unib,uniy,unim):

    """ Esta función grafica la gráfica de enerigía específica \n
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
        plot: Gráfica de energía específica[m]
    """
    
    x = np.linspace(0,10,10)
    yg = np.linspace(0.2,10,300) 

    A = Area(b,yg,m1,m2,unib,uniy,unim)
    Q = Qfun(v1,b,y,m1,m2,unib,uniy,unim)
  
    
    Ei = yg + (Q)**2/(2*g*(A)**2)  

    plt.style.use('classic')
    plt.plot(Ei,yg,label = 'S')
    plt.plot(x,x, label = 'E = y', linestyle='dashed')
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend(loc='upper left')
    plt.show()

    
def grafica2_txt (v1,b,y,m1,m2,g,unib,uniy,unim, ruta):

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
    Q = Qfun(v1,b,y1,m1,m2,unib,uniy,unim)
    
    file = open(ruta, 'w')
   
    for index in range(len(yg)):
        
        A = Area(b,yg[index],m1,m2,unib,uniy,unim)
        
        Ei = yg[index] + (Q)**2/(2*g*(A)**2)  
        
        file.write(str(yg[index]) + ";" + str(Ei) + "\n")
        
    file.write("Linea Recta\n")
    
    for index in range(len(x)):
        
        file.write(str(x[index]) + ";" + str(x[index]) + "\n")
        
    file.close()
    
    
    

def imprimir_valores(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2):
    
    """ Esta función retorna los valores del caudal, el área y la gráfica
    Retorna:
        plot: Gráfica de energía específica
        str: Mensaje con los valores de caudal y área
    """
    
    b = cambio_unidades(unib,b)
    y1 = cambio_unidades(uniy,y1)
    z1 = cambio_unidades(uniz1,z1)
    z2 = cambio_unidades(uniz2,z2)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    
    grafica2(v1, b, y1, m1, m2, g, unib, uniy, unim)
    yf = y2fun(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2)
    
    i=0
    y =[]
    
    while i<len(yf):
        
        y.append(round(yf[i],3))
        i+=1
    
    msg1 = '\nEl área transversal 1 es: '+str(round(Area(b, y1, m1, m2, unib, uniy, unim),3)) 
    
    if b!=0 and m1 !=0 and m2 != 0:
        msg2 = '\nEl área transversal 2 es: '+str(round(Area(b, max(yf), m1, m2, unib, uniy, unim),3)) 
    else:
        msg2 = '\nEl área transversal 2 es: '+str(round(Area(b, y[2], m1, m2, unib, uniy, unim),3)) 
    
    msg3 = '\nEl cuadal [l/s] es:'+str(round(Q_en_litros(v1, b, y1, m1, m2, unib, uniy, unim),4)) 
    msg4 = '\nLos valores de y2 son: '+ str(y2fun(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2))
    msg5 = '\nEl valor final de y2 es: '+ str(y2_final_valor(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2))
    
    
    temp = msg1 +msg2 + msg3 +msg4 +msg5
    
    return temp


def valores(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2):
    
   
    temp = ''
    
    b = cambio_unidades(unib,b)
    y1 = cambio_unidades(uniy,y1)
    z1 = cambio_unidades(uniz1,z1)
    z2 = cambio_unidades(uniz2,z2)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    
    A1 = Area(b,y1,m1,m2,unib,uniy,unim)
    
    Q = Qfun(v1,b,y1,m1,m2,unib,uniy,unim)
    
    QL = Q_en_litros(v1,b,y1,m1,m2,unib,uniy,unim)
    
    y_2 = y2fun(y2,b,y1,m1,m2,v1,z1,z2,g,unib,uniy,unim,uniz1,uniz2)
    
    y_2_final = y2_final_valor(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2)
    
    A2 = Area(b,y_2_final,m1,m2,unib,uniy,unim)
    
    print(A1, Q, QL, y_2,y_2_final,A2)
    
    return temp

unib = 'm'
uniy = 'm'
uniz1 = 'm'
uniz2 = 'm'
unim = ''
ruta = './seconocey1.txt'

b=10
y1=4.5
v1=1.25
z1=0
z2=1.05
m1=0
m2=0
g = 9.81


#print(imprimir_valores(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2))
#print(valores(y2, b, y1, m1, m2, v1, z1, z2, g, unib, uniy, unim, uniz1, uniz2))
#print(grafica2_txt (v1,b,y,m1,m2,g,unib,uniy,unim, ruta))






























