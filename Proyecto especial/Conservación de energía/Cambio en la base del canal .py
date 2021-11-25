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
yin, m, yc, Ec, y2, v2, At= symbols('yin m yc Ec y2 v2 At')

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

def Area(y,b,m1,m2,uniy,unib,unim):
    
    """ Esta función retorna el área transversal según la figura\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unib Unidades de la base propiedades (mm,cm,m,in)
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
            
    if b!= 0 and m1 != 0 and m2 != 0:
        
        
        if m1 == m2:
                
            A = (b+m1*y)*y
                
        else:
                
            A = m1*y**2/2+b*y+m2*y**2/2 
            
    return A



def Tfun(y,b,m1,m2,uniy,unib,unim):
    
    """ Esta función retorna el espejo de agua según la sección transversal\n
        
    Parámetros:
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unib Unidades de la base propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: El espejo de agua de la sección transversal [m]
    """

    y = cambio_unidades(uniy,y)
    b = cambio_unidades(unib,b)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)

    if m1 == 0 and m2 == 0:
        
        T = b

    if b!= 0 and m1 != 0 and m2 != 0:
        
        
        if m1 == m2:
                
            T = b + 2 * (m1*y)
                
        else:
                
            T = b + (m1*y) + (m2*y)

    return T
    

def Qfun(v1,y,b,m1,m2,uniy,unib,unim):
    
    """ Esta función retorna el caudal según la sección transversal\n
        
    Parámetros:
        v1 (float) Velocidad de la sección 1
        y (float) altura del agua
        b (float) base del canal
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unib Unidades de la base propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: El cuadal de la sección transversal [m^3/s]
    """
    
    Q = v1 * Area(y,b,m1,m2,uniy,unib,unim) 
    
    return Q


def y2fun(y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim):
    
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
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unib1 Unidades de la base1 propiedades (mm,cm,m,in)
        unib2 Unidades de la base2 propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: La altura del agua en la sección 2 [m]
    """
    y1 = cambio_unidades(uniy,y1)
    b1 = cambio_unidades(unib1,b1)
    b2 = cambio_unidades(unib2,b2)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    Q = Qfun(v1,y1,b1,m1,m2,uniy,unib1,unim)
    
    if m1 == 0 and m2 == 0:
        
        ec1 = Eq(y1+((v1**2)/(2*g)),y2+((Q**2)/(2*g*(b2*y2)**2)))
    
        y2 = solve(ec1)  
    
    if b1!= 0 and m1 != 0 and m2 != 0:
        
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



def calculo_yc(yc,y1,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim):
    
    """ Esta función retorna la altura crítica del agua\n
        
    Parámetros:
        yc (symbol) variable que se quiere calcular
        y1 (float) altura del agua de la sección 1
        v1 (float) Velocidad de la sección 1
        b1 (float) base del canal en la sección 1
        b2 (float) base del canal en la sección 2
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unib1 Unidades de la base1 propiedades (mm,cm,m,in)
        unib2 Unidades de la base2 propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: La altura crítica del agua [m]
    """
    
    Q = Qfun(v1,y1,b1,m1,m2,uniy,unib1,unim)
    
    A = Area(yc,b2,m1,m2,uniy,unib2,unim)
    
    T = Tfun(yc,b2,m1,m2,uniy,unib2,unim)
    
    ec1 = Eq(Q/sqrt(g),(A*sqrt(A))/sqrt(T))
            
    yc = solve(ec1)[0]
    
    return yc



def calculo_v2(y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim):
    
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
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unib1 Unidades de la base1 propiedades (mm,cm,m,in)
        unib2 Unidades de la base2 propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: La velocidad del agua en la sección 2 [m]
    """
    
    y_2 = y2fun(y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)
    Q = Qfun(v1,y1,b1,m1,m2,uniy,unib1,unim)
    
    if y_2 == "Fenomeno de choque, se requiere calcular yc\n":
        
        y_c = calculo_yc(yc,y1,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)
        A = Area(y_c,b2,m1,m2,uniy,unib2,unim)
        
        ecu = Eq(Q,v2*A)
        v = solve(ecu)
    else:
        if m1 == 0 and m2 == 0:
            
            A = Area(y_2[2],b2,m1,m2,uniy,unib2,unim)
            
            ecu = Eq(Q,v2*A)
            v = solve(ecu)
            
        if b1!= 0 and m1 != 0 and m2 != 0:
            
            A = Area(max(y_2),b2,m1,m2,uniy,unib2,unim)
            
            ecu = Eq(Q,v2*A)
            v = solve(ecu)
    
    return v


def calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim):

    """ Esta función retorna la velocidad del agua en la sección dos\n     
    Parámetros:
        Ec (symbol) variable que se quiere calcular
        yc (float) altura critica del agua
        y1 (float) altura del agua de la sección 1
        y2 (float) altura del agua de la sección 2
        v1 (float) Velocidad de la sección 1
        b1 (float) base del canal en la sección 1
        b2 (float) base del canal en la sección 2
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unib1 Unidades de la base1 propiedades (mm,cm,m,in)
        unib2 Unidades de la base2 propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: La velocidad del agua en la sección 2 [m]
    """
    
    y_c = calculo_yc(yc,y1,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)
    v_2 = calculo_v2(y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)[0]
    
    ecu = Eq(Ec,y_c + v_2**2/(2*g))
    
    Ec = solve(ecu)
    
    return Ec

def calculo_yin(Ec,yin,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim):
    
    """ Esta función retorna la nueva altura inicial del agua \n     
    Parámetros:
        Ec (symbol) variable que se quiere calcular
        yin (symbol) variable que se requiere calcular
        y1 (float) altura del agua de la sección 1
        y2 (float) altura del agua de la sección 2
        v1 (float) Velocidad de la sección 1
        b1 (float) base del canal en la sección 1
        b2 (float) base del canal en la sección 2
        m1 (float) grados o inclinación parte izquierda de un trapecio
        m2 (float) grados o inclinación parte derecha de un trapecio
        g (float) Aceleración gravitacional, generalmente 9.81 
        uniy Unidades de la altura propiedades (mm,cm,m,in)
        unib1 Unidades de la base1 propiedades (mm,cm,m,in)
        unib2 Unidades de la base2 propiedades (mm,cm,m,in)
        unim Unidades de inclinación (grados,radianes,m)
    Retorna:
        float: La velocidad del agua en la sección 2 [m]
    """
    
    Q = Qfun(v1,y1,b1,m1,m2,uniy,unib1,unim)
    Ec = calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)[0]

    if m1 == 0 and m2 == 0:
        
        ec1 = Eq(Ec,yin+((Q**2)/(2*g*(b1*yin)**2)))
    
        yin = solve(ec1)  
    
    if b1 == 0 and m1 != 0 and m2 != 0:
        
        if m1 == m2:
                
            ec1 = Eq(Ec,yin+((Q**2)/(2*g*((b1+m1*yin)*yin)**2)))
    
            yin = solve(ec1)
                
        else:
            ec1 = Eq(Ec,yin+((Q**2)/(2*g*(m1*yin**2/2+b1*yin+m2*yin**2/2)**2)))
        
            yin = solve(ec1)
    i=0
    y =[]
    
    while i<len(yin):

        y.append(round(re(yin[i]),3))
            
        i+=1
        
    return y


def grafica4 (Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim):

    Q = Qfun(v1,y1,b1,m1,m2,uniy,unib1,unim)
    EqCri = Eq(m,(0-calculo_yc(yc,y1,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim))/(0-calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)[0]))
    m = solve(EqCri)

    x = np.linspace(0,10,50)

    yg = np.linspace(0.1,10,1000)
    
    E = yg + (Q**2/(2*g*(Area(yg,b1,m1,m2,uniy,unib1,unim))**2))
    E2 = yg + (Q**2/(2*g*(Area(yg,b2,m1,m2,uniy,unib2,unim))**2))
    

    plt.style.use('ggplot')
    plt.plot(E,yg,label = 'S1')
    plt.plot(E2,yg,label = 'S2')
    plt.plot(x,x, label = 'E = y',linestyle='dashed')
    if m1 == 0 and m2 == 0:
        plt.plot(x,m*x,label = 'Ec = 3/2 yc', linestyle='dashed')
        
    plt.xlabel('E (m)')
    plt.ylabel('y (m)')
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.legend()
    plt.show()


def grafica4_txt (Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim,ruta):

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
    Q = Qfun(v1,y1,b1,m1,m2,uniy,unib1,unim)
    EqCri = Eq(m,(0-calculo_yc(yc,y1,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim))/(0-calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)[0]))
    m = solve(EqCri)
    
    
    
    file = open(ruta, 'w')
   
    file.write("S1\n")
    for index in range(len(yg)):
        
        A1 = Area(yg[index],b1,m1,m2,uniy,unib1,unim)
        
        Ei1 = yg[index] + (Q)**2/(2*g*(A1)**2)  
        
        file.write(str(yg[index]) + ";" + str(Ei1) + "\n")
        
    
    file.write("S2\n")
    
    for index in range(len(yg)):
        
        A2 = Area(yg[index],b2,m1,m2,uniy,unib2,unim)
        
        Ei2 = yg[index] + (Q)**2/(2*g*(A2)**2)  
        
        file.write(str(yg[index]) + ";" + str(Ei2) + "\n")
    
    file.write("Linea Recta\n")
    
    for index in range(len(x)):
        
        file.write(str(x[index]) + ";" + str(x[index]) + "\n")
        
    
    if m1 == 0 and m2 == 0:
        
        file.write("Ec = 3/2 yc\n")
    
        for index in range(len(x)):
        
            file.write(str(x[index]) + ";" + str(x[index]*m[0]) + "\n")
    
    file.close()

def imprimir_valores(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim):
    
    msg1 = '\nArea1 '+ str( Area(y1,b1,m1,m2,uniy,unib1,unim))
    
    msg2 = '\nCaudal '+ str(Qfun(v1,y1,b1,m1,m2,uniy,unib1,unim))
    
    msg3 = '\nvalores de y2 '+ str(y2fun(y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim))
    
    msg4 = '\nvalor de yc'+ str(calculo_yc(yc,y1,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim))
    
    msg5 = '\nvalor de Ec'+ str(calculo_Ec(Ec,yc,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim))

    msg6 = '\nvelocidad en 2 '+ str(calculo_v2(y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim))   
    
    msg7= '\nNuevo y1 '+ str( max(calculo_yin(Ec,yin,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)))
   
    grafica4(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)
    
    return msg1 + msg2 + msg3+ msg4+ msg5+ msg6+ msg7
    

def valores(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim):
    
    temp = ''
    Q = Qfun(v1,y1,b1,m1,m2,uniy,unib1,unim)
    b1 = cambio_unidades(unib1,b1)
    b2 = cambio_unidades(unib2,b2)
    m1 = cambio_angulo(unim,m1)
    m2 = cambio_angulo(unim,m2)
    y1 = cambio_unidades(uniy,y1) 
    
    A1 = Area(y1,b1,m1,m2,uniy,unib1,unim)
    
    QL = Q*1000
    
    y_2 = y2fun(y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)
    
    y_c = calculo_yc(yc,y1,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)
    
    if y_2 == "Fenomeno de choque, se requiere calcular yc\n":
        
        y_c = calculo_yc(yc,y1,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)
    
    A2 = float(solve(Eq(Q,calculo_v2(y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim)[0]*At))[0])
    
    print(y1,A1, Q, QL, y_2,y_c,A2)
    
    return temp

unib1 = 'm'
unib2 = 'm'
uniy = 'm'
uniz1 = 'm'
uniz2 = 'm'
unim = ''
ruta = 'D:\Documents\Hidraulica-APP\Proyecto especial\Conservación de energía/cambioenlabasedelcanal.txt'

y1=3.8
b1=16
b2=10
v1=1.05
z1=0
z2=0
m1=0
m2=0
g=9.81

print(imprimir_valores(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim))
print(valores(Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim))
print(grafica4_txt (Ec,yc,m,y1,y2,v1,b1,b2,m1,m2,g,uniy,unib1,unib2,unim, ruta))












