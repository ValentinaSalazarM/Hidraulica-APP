# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 12:59:07 2021

@author: Gabriela Bermudez
"""

'Importar librerias'
import numpy as np
import matplotlib.pyplot as plt
import math
import sys
import unidecode
import scipy.integrate as integrate

'-----------------------------------------------------------------------------'
'Funciones para cambio de unidades'

def CU_m(x,u):
    """Cambia unidades de longitud ingresadas a metros \n
    x=valor
    u=unidades --> cm, mm, in"""
    if u=='mm':
        var=x/1000
    elif u=='cm':
        var=x/100
    elif u=='in':
        var=x*0.0254
    else:
        var=x
    return var

def CU_theta(x,u):
    """Cambia unidades de ángulo ingresado a grados \n
    x=valor
    u=unidades --> grados, radianes, m/m """
    if u=='grados':
        theta=x
    elif u=='radianes':
        theta=math.degrees(x)
    else:
        theta=math.degrees((math.atan(x)))
        
    return theta


'-----------------------------------------------------------------------------'
'Funciones que retornan geometría del canal'

def  geom_c(d,ynd,ud):
    """ Esta función retorna la geometría de un canal circular\n
    d=diametro<br />
    ynd=relación de llenado<br />
    unidades=unidades de d (mm, cm, m, in)<br />"""
    
    d = CU_m(d,ud)

    
    yn=ynd*d
    theta = math.pi+2*math.asin((yn-(d/2))/(d/2))
    A= (theta-math.sin(theta))*d**2/8
    P= theta*d/2
    Rh=(1-math.sin(theta)/theta)*d/4
    T=d*math.cos(math.asin((yn-(d/2))/(d/2)))
    D=A/T
    return yn,theta,A,P,Rh,T,D

def geom_r(y,b,m1,m2,um,uy,ub):
    """ Esta función retorna la geometría de un canal geométrico no circular\n
    y=profundidad<br />
    b=base<br />
    m1=inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)
    uy=unidades de y (mm, cm, m, in)<br />
    ub=unidades de b (mm, cm, m, in)<br />"""
    
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
    
    y=CU_m(y,uy)
    b=CU_m(b,ub)
    
    A = b*y+(m1*y**2)/2+(m2*y**2)/2
    P=b+y*math.sqrt(m1**2+1)+y*math.sqrt(m2**2+1)
    Rh=A/P
    T=b+m1*y+m2*y
    D=A/T
    return A,P,Rh,T,D

'-----------------------------------------------------------------------------'
def froude(y,b,m1,m2,um,Q,v,d,uy,ub,ud,uQ):
    """Calcula el número de froude con las propiedades geométricas y el caudal\n
    y=profundidad (m)<br />
    b=base (m)<br />
    m1=inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    Q=caudal (m3/s) <br />
    v = velocidad (m/s) <br />
    d=diámetro (m)<br />
    u_y=unidades de y (mm, cm, m, in)<br />
    u_b=unidades de b (mm, cm, m, in)<br />
    u_d=unidades de d (mm, cm, m, in)<br />
    u_Q = unidades de caudal--> L, m3 <br />
    Los parámetros que no se requieran, se dejan en 0"""
    
    y=CU_m(y,uy)
    b=CU_m(b,ub)
    d=CU_m(d,ud)
    if uQ=='L':
        Q=Q/1000
    
    if d==0:
        A,P,Rh,T,D=geom_r(y,b,m1,m2,um,"m","m")
    else:
        ynd=y/d
        yn,theta,A,P,Rh,T,D=geom_c(d,ynd,"m")
    
    if v!=0:
        Fr = v/(math.sqrt(9.81*A/T))
    elif Q!=0:
        Fr=Q/(A*math.sqrt(9.81*A/T))
    else:
        raise Exception ("Faltan datos")
    return Fr

'-----------------------------------------------------------------------------'
def ecuacion_yc_Rectangulo(Q,v,b,m1,m2,y):
    if Q!=0:
        ecuacion=((Q/math.sqrt(9.81))-(b*y+(m1*y**2)/2+(m2*y**2)/2)*math.sqrt(b*y+(m1*y**2)/2+(m2*y**2)/2)/(math.sqrt(b+m1*y+m2*y)))
    elif v!=0:
        ecuacion=v/math.sqrt(9.81)-((b*y+(m1*y**2)/2+(m2*y**2)/2)/(b+m1*y+m2*y))^(1/2)
    else:
        raise Exception ("faltan datos")
    return ecuacion

def derivada_yc_Rectangulo(Q,v,b,m1,m2,y):
    if Q!=0:
        derivada=((m1+m2)*(b*y+(m1*y**2)/2+(m2*y**2)/2)**(3/2))/(2*(b+m1*y+m2*y)**(3/2)) - (3/2)*math.sqrt(b+m1*y+m2*y)*math.sqrt(b*y+(m1*y**2)/2+(m2*y**2)/2)
    elif v!=0:
        derivada=-(1-((m1+m2)*(b*y+(m1*y**2)/2+(m2*y**2)/2))/(b+m1*y+m2*y)**2)/(2*math.sqrt((b*y+(m1*y**2)/2+(m2*y**2)/2)/(b+m1*y+m2*y)))
    else:
        raise Exception ("faltan datos")

    return derivada

def ecuacion_yc_Circulo(Q,v,d,y):
    if Q!=0:
        ecuacion=(Q/math.sqrt(9.81))-((((d**2)/8)*(math.pi+2*math.asin((y-(d/2))/(d/2))-math.sin(math.pi+2*math.asin((y-(d/2))/(d/2)))))**(3/2)/(d*math.sin((math.pi+2*math.asin((y-(d/2))/(d/2)))/2))**(1/2))
    elif v!=0:
        ecuacion=(Q/math.sqrt(9.81))-((((d**2)/8)*(math.pi+2*math.asin((y-(d/2))/(d/2))-math.sin(math.pi+2*math.asin((y-(d/2))/(d/2)))))**(1/2)/(d*math.sin((math.pi+2*math.asin((y-(d/2))/(d/2)))/2))**(1/2))
    return ecuacion

def derivada_yc_Circulo(Q,v,d,y):
    if Q!=0:
        derivada=((d**2*(2*math.asin((2*(y-d/2))/d)+math.sin(2*math.asin((2*(y-d/2))/d))+math.pi))**(3/2)*math.cos(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi)))/(16*math.sqrt(2)*math.sqrt(1-(4*(y-d/2)**2)/d**2)*(d*math.sin(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi)))**(3/2))-(3*d**2*math.sqrt(d**2*(2*math.asin((2*(y-d/2))/d)+math.sin(2*math.asin((2*(y-d/2))/d))+math.pi))*(4/(d*math.sqrt(1-(4*(y-d/2)**2)/d**2))+(4*math.cos(2*math.asin((2*(y-d/2))/d)))/(d*math.sqrt(1-(4*(y-d/2)**2)/d**2))))/(32*math.sqrt(2)*math.sqrt(d*math.sin(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi))))        
    elif v!=0:
        derivada=(math.sqrt(d**2*(2*math.asin((2*(y-d/2))/d)+math.sin(2*math.asin((2*(y-d/2))/d))+math.pi))*math.cos(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi)))/(2*math.sqrt(2)*math.sqrt(1-(4*(y-d/2)**2)/d**2)*(d*math.sin(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi)))**(3/2))-(d**2*(4/(d*math.sqrt(1-(4*(y-d/2)**2)/d**2))+(4*math.cos(2*math.asin((2*(y-d/2))/d)))/(d*math.sqrt(1-(4*(y-d/2)**2)/d**2))))/(4*math.sqrt(2)*math.sqrt(d**2*(2*math.asin((2*(y-d/2))/d)+math.sin(2*math.asin((2*(y-d/2))/d))+math.pi))*math.sqrt(d*math.sin(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi))))
    return derivada

def yc(Q,b,v,m1,m2,um,d,ub,ud,uQ):  
    """Calcula la profundidad crítica. Para secciones rectángulares se recurre a una solución analítica. Para las demás se recurre a una solución numérica (Newton-Raphson)\n
    Q = caudal (m3/s) <br />
    b = base (m) <br />
    v= velocidad m/s <br />
    m1 = inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    d = diámetro (m) \n  
    u_b=unidades de b (mm, cm, m, in)<br />
    u_d=unidades de d (mm, cm, m, in)<br />
    u_Q = unidades de caudal--> L, m3 <br />
    Los parámetros que no se requieran, se dejan en 0"""
    
    b=CU_m(b,ub)
    d=CU_m(d,ud)
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
    
    if uQ=='L':
        Q=Q/1000

    
    if d==0:        
        if m1==0 and m2==0:
            yc=((Q**2)/(9.81*(b**2)))**(1/3)
        else:
            error=1
            y=b
            
            while error>0.0001:
                yc=y-ecuacion_yc_Rectangulo(Q,v,b,m1,m2,y)/derivada_yc_Rectangulo(Q,v,b,m1,m2,y)
                error=abs(yc-y)
                y=yc
    else:
        error=1
        y=d/2
        while error>0.0001:
            yc=y-ecuacion_yc_Circulo(Q,v,d,y)/derivada_yc_Circulo(Q,v,d,y)
            error=abs(yc-y)
            y=yc

    return float(yc)

'-----------------------------------------------------------------------------'
def vc (m1,m2,um,b,yc,d,uy,ub,ud):
    """Calcula la velocidad crítica a partir de Froude y geometría crítica\n
    m1 = inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    b = base (m) <br>
    yc = profundidad crítica (m) <br>
    d = diámetro (m) \n
    u_y=unidades de y (mm, cm, m, in)<br />
    u_b=unidades de b (mm, cm, m, in)<br />
    u_d=unidades de d (mm, cm, m, in)<br />
    
    Los parámetros que no sean necesarios se dejan en 0"""
    yc=CU_m(yc,uy)
    b=CU_m(b,ub)
    d=CU_m(d,ud)
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
    
    if d==0:
        A,P,Rh,T,D=geom_r(yc,b,m1,m2,um,"m","m")
    else:
        ynd=yc/d
        yn,theta,A,P,Rh,T,D=geom_c(d,ynd,"m")
    
    v=math.sqrt(9.81*A/T)
    return v
    
'-----------------------------------------------------------------------------'
def momentum(Q,b,m1,m2,um,y,d,uQ,ub,uy,ud):
    """Calcula momentum de una sección a partir de geometría y caudal\n
    Q = caudal (m3/s) <br />
    y = profundidad <br />
    b = base (m) <br />
    m1 = inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    d = diámetro (m) <br />
    u_y=unidades de y (mm, cm, m, in)<br />
    u_b=unidades de b (mm, cm, m, in)<br />
    u_d=unidades de d (mm, cm, m, in)<br />
    u_Q = unidades de caudal--> L, m3 <br />"""   
    
    y=CU_m(y,uy)
    b=CU_m(b,ub)
    d=CU_m(d,ud)
    if uQ=='L':
        Q=Q/1000
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
        
    if d==0:        
        if m1==0 and m2==0:
            mom=y**2/2+(Q/b)**2/(9.81*y)
        
        else:
            mom=m1*y**3/6+m2*y**3/6+b*y**2/2+Q**2/(9.81*(b*y+(m1*y**2)/2+(m2*y**2)/2))
    
    else:
        theta = math.pi+2*math.asin((y-(d/2))/(d/2))
        mom=d**3/24*(3*math.sin(theta/2)-(math.sin(theta/2))**3-3*(theta/2)*math.cos(theta/2))+Q**2/(9.81*d**2*(theta-math.sin(theta))/8)
    return float(mom)


'-----------------------------------------------------------------------------'
'    Falta probar los no rectangulares'

def fuerzaCompuerta(y1,y2,b,Q,m1,m2,um,rho,uy1,uy2,ub,uQ):
    """Calcula fuerza sobre la compuerta en canales primáticos\n
    y1= profundidad de sección 1 <br />
    y2= profundidad de sección 2 <br />
    b = base (m) <br />
    Q = caudal (m3/s) <br />
    m1 = inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    rho = densidad (kg/m3)
    uy1=unidades de y1 (mm, cm, m, in)<br />
    uy2=unidades de y1 (mm, cm, m, in)<br />
    ub=unidades de b (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    """
    y1=CU_m(y1,uy1)
    y2=CU_m(y2,uy2)
    ub=CU_m(b,ub)
    if uQ=='L':
        Q=Q/1000
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
    
    M1=momentum(Q,b,m1,m2,um,y1,0,"","m","m","m")
    M2=momentum(Q,b,m1,m2,um,y2,0,"","m","m","m")
    
    if m1==0 and m2==0:
        f=rho*9.81*b*(M1-M2)
    else:
        f=rho*9.81*(M1-M2)
    return M1,M2,f


'-----------------------------------------------------------------------------'
# def ecuacionTriangulo(Q,m,y1,y2,f):
#     ecuacion= ((1/3)*(y1**3-y2**3)+(Q**2/(9.81*m)*((1/y1**2)-(1/y2**2)))-f)/(y2-y1)
#     return ecuacion
# def derivadaTriangulo(Q,m,y1,y2,f):
#     derivada=((2*Q**2)/(9.81*m*y2**3)-y2**2)/(y2-y1)-(-f+(Q**2*(1/y1**2-1/y2**2))/(9.81*m)+1/3*(y1**3-y2**3))/(y2-y1)**2
#     return derivada


# def ecuacionTrapecio(Q,m,b,y1,y2,f):
#     ecuacion=((m/3)*(y1**3-y2**3)+(b/2)*(y1**2-y2**2)+(Q**2/9.81)*((1/(m*y1**2+b*y1))-(1/(m*y2**2+b*y2)))-f)/(y2-y1)
#     return ecuacion 
# def derivadaTrapecio(Q,b,m,y1,y2,f):
#     derivada=((Q**2*(b+2*m*y2))/(9.81*(b*y2+m*y2**2)**2)-b*y2-m*y2**2)/(y2-y1)-((Q**2*(1/(b*y1+m*y1**2)-1/(b*y2+m*y2**2)))/9.81+(1/2)*b*(y1**2-y2**2)+1/3*m*(y1**3-y2**3)-f)/(y2-y1)**2
#     return derivada

def ecuacionSubsecuente(Q,b,m1,m2,y1,y2,f):
    ecuacion = ((1/6)*(m1*y1**3+m2*y1**3-m1*y2**3-m2*y2**3)+(b/2)*(y1**2-y2**2)+(Q**2/(9.81*((m1*y1**2+m2*y1**2)/2+b*(y1))))-(Q**2/(9.81*((m1*y2**2+m2*y2**2)/2+b*(y2))))-f)/(y2-y1)
    return ecuacion
def derivadaSubsecuente(Q,b,m1,m2,y1,y2,f):
    #derivada = (-(2*y2**6*9.81*(m1+m2)**3+y2**5*(11*b-(m1+m2)*y1)*9.81*(m1+m2)**2+5*y2**4*(4*b**2-3*b*(m1+m2)*y1-(m1+m2)**2*y1**2)*9.81*(m1+m2)+2*y2**3*(6*b**3-22*b**2*(m1+m2)*y1-7*b*(m1+m2)**2*y1**2-(3*f-(m1+m2)*y1**3)*(m1+m2)**2)*9.81-2*y2**2*(18*b**3*y1-6*b**2*(m1+m2)*y1**2+b*(12*f-11*(m1+m2)*y1**3)*(m1+m2)+(3*f-2*(m1+m2)*y1**3)*(m1+m2)**2*y1)*9.81+y2*(36*b**3*9.81*y1**2-4*b**2*(6*f-7*(m1+m2)*y1**3)*9.81+3*b*9.81*(m1+m2)**2*y1**4+(6*f*9.81*(m1+m2)*y1**2-9.81*(m1+m2)**2*y1**5-36*Q**2)*(m1+m2))-12*b**3*9.81*y1**3+8*b**2*(3*f-2*(m1+m2)*y1**3)*9.81*y1+b*(24*f*9.81*(m1+m2)*y1**2-7*9.81*(m1+m2)**2*y1**5-48*Q**2)+(6*f*9.81*(m1+m2)*y1**2-9.81*(m1+m2)**2*y1**5-12*Q**2)*(m1+m2)*y1))/(6*(y2-y1)**2*(y2*(m1+m2)+2*b+(m1+m2)*y1)*(y2**2*(m1+m2)+2*y2*b-(2*b+(m1+m2)*y1)*y1)*9.81)
    derivada = (-(2*y2**7*(2*b+(m1+m2)*y1)*9.81*(m1+m2)**3*y1+y2**6*(2*b+(m1+m2)*y1)*(11*b-3*(m1+m2)*y1)*9.81*(m1+m2)**2*y1+2*y2**5*b*(2*b+(m1+m2)*y1)*(10*b-9*(m1+m2)*y1)*9.81*(m1+m2)*y1+y2**4*(24*b**4*9.81*y1-60*b**3*9.81*(m1+m2)*y1**2-30*b**2*9.81*(m1+m2)**2*y1**3-b*(12*f-5*(m1+m2)*y1**3)*9.81*(m1+m2)**2*y1-(6*f*9.81*(m1+m2)*y1**2-9.81*(m1+m2)**2*y1**5-12*Q**2)*(m1+m2)**2)-4*y2**3*b*(12*b**3*9.81*y1**2+b*(12*f-5*(m1+m2)*y1**3)*9.81*(m1+m2)*y1+(6*f*9.81*(m1+m2)*y1**2-9.81*(m1+m2)**2*y1**5-12*Q**2)*(m1+m2))+4*y2**2*(6*b**4*9.81*y1**3-b**3*(12*f-5*(m1+m2)*y1**3)*9.81*y1-b**2*(6*f*9.81*(m1+m2)*y1**2-9.81*(m1+m2)**2*y1**5-12*Q**2)-18*b*Q**2*(m1+m2)*y1-9*Q**2*(m1+m2)**2*y1**2)-24*y2*(4*b**2-(m1+m2)**2*y1**2)*Q**2*y1+24*b*(2*b+(m1+m2)*y1)*Q**2*y1**2))/(6*y2**2*(y2-y1)**2*(y2*(m1+m2)+2*b)**2*(2*b+(m1+m2)*y1)*9.81*y1)
    return derivada
    
def y_subsecuente(Q,b,m1,m2,um,y1,f,uy1,ub,uQ):
    """Calcula profundidad subsecuente por medio de conservación del momento. Para canales rectangulares se utiliza la solución analítica. Para los demás se recurre a una solución numérica (Newton Raphson).\n
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    m1 = inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    y1 = profundidad de sección 1 <br>
    f=fuerza aplicada en caso de resalto forzado (si no es forzado, poner 0)
    ub = unidades de b (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    uy1 = unidades y1 (mm ,cm ,m , in)"""
    
    y1=CU_m(y1,uy1)
    b=CU_m(b,ub)
    if uQ=='L':
        Q=Q/1000
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
    
    if m1==0 and m2==0:
        Fr=froude(y1,b,0,0,"",Q,0,0,"m","m","m","m3/s")
        #froude(y1,b,m,Q,0,0,"m","m","m3")
        y2=y1/2*(math.sqrt(1+8*Fr**2)-1)
    # elif b==0:
    #     error=1
    #     y=2*y1
    #     while error>0.0001:
    #         y2=y-ecuacionTriangulo(Q,m,y1,y,f)/derivadaTriangulo(Q,m,y1,y,f)
    #         error=abs(y2-y)
    #         y=y2
    # else:
    #     error=1
    #     y=2*y1
    #     while error>0.0001:
    #         y2=y-ecuacionTrapecio(Q,m,b,y1,y,f)/derivadaTrapecio(Q,b,m,y1,y,f)
    #         error=abs(y2-y)
    #         y=y2
    else:
        error=1
        y=4*y1
        while error>0.0001:
            num=ecuacionSubsecuente(Q,b,m1,m2,y1,y,f)
            den=derivadaSubsecuente(Q,b,m1,m2,y1,y,f)
            y2=y-num/den
            error=abs(y2-y)
            y=y2
    return y2

'-----------------------------------------------------------------------------'
def eficienciaRH(Q,b,m1,m2,um,y1,f,uy1,ub,uQ):
    """Calcula eficiencia del RH a partir del caudal, geometría aguas arriba y fuerza en caso de ser forzado\n
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    m1 = inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    y1 = profundidad en sección 1 <br>
    f = fuerza aplicada en caso de resalto forzado (si no es forzado, poner 0)
    ub = unidades de b (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    uy1 = unidades y1 (mm ,cm ,m , in)"""
    
    y1=CU_m(y1,uy1)
    b=CU_m(b,ub)
    if uQ=='L':
        Q=Q/1000
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
    
    y2=y_subsecuente(Q,b,m1,m2,"m",y1,f,"m","m","m3/s")
    
    A1,P1,Rh1,T1,D1=geom_r(y1,b,m1,m2,"m","m","m")
    A2,P2,Rh2,T2,D2=geom_r(y2,b,m1,m2,"m","m","m")
        
    E1=y1+Q**2/(2*9.81*A1**2)
    E2=y2+Q**2/(2*9.81*A2**2)+f
    
    eficiencia=abs(E1-E2)/E1*100
    
    return (E1, E2), (eficiencia,)

'-----------------------------------------------------------------------------'
def eficienciaRHI(Q,b,m1,m2,um,y1,yn,l,i,uQ,ub,uy1,ul,ui):
    """Calcula eficiencia del RH inclinado a partir del caudal, geometría aguas arriba, inclinación del canal y longitud de la parte inclinada del canal (utilizar gráfica)\n
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    m1 = inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    y1 = profundidad en sección 1 <br>
    l = longitud de la parte inclinada del resalto (m) <br>
    i = inclinación del canal (grados, radianes, m/m)
    ub = unidades de b (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    uy1 = unidades y1 (mm ,cm ,m , in) <br />
    ul = unidades de longitud--> (mm ,cm ,m , in) 
    ui = unidades de inclinacion--> grados, radianes, m/m <br />"""
    
    y1=CU_m(y1,uy1)
    b=CU_m(b,ub)
    l=CU_m(l,ul)
    if uQ=='L':
        Q=Q/1000
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
        
    inclinacion=CU_theta(i,ui)

    
    z=l*math.tan(math.radians(inclinacion))
    A1,P1,Rh1,T1,D1=geom_r(y1,b,m1,m2,"m","m","m")
    A2,P2,Rh2,T2,D2=geom_r(yn,b,m1,m2,"m","m","m")

    E1=y1+Q**2/(2*9.81*A1**2)+z
    E2=yn+Q**2/(2*9.81*A2**2)
    
    eficiencia=abs(E1-E2)/E1*100
    
    return (E1, E2, z), (eficiencia,)
'-----------------------------------------------------------------------------'
def clasificacionResalto(Q,b,m1,m2,d,ud,um,y,ub,uy,uQ):
    """Clasifica resalto con el número de Froude a partir de las propiedades geométricas aguas arriba\n
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    m1 = inclinación lado 1<br />
    m2 = inclinación lado 2<br />
    um = unidades de m (grados, radianes, m/m)<br />
    y = profundidad aguas arriba <br />
    ub = unidades de b (mm, cm, m, in)<br />
    uy = unidades de y (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3"""
    
    y=CU_m(y,uy)
    b=CU_m(b,ub)
    d=CU_m(y,ud)
    if uQ=='L':
        Q=Q/1000
    m1=CU_theta(m1,um)
    m2=CU_theta(m2,um)
    m1=math.tan(math.radians(m1))
    m2=math.tan(math.radians(m2))
    
    Fr=froude(y,b,m1,m2,"m",Q,0,d,"m","m","m","m3/s")
    if Fr<1:
        return (Fr,),('Flujo subcrítico',)
    elif Fr<=1.7:
        return (Fr,),('RH ondular')
    elif Fr<=2.5:
        return (Fr,),('RH débil')
    elif Fr<=4.5:
        return (Fr,),('RH oscilante')
    elif Fr<=9:
        return (Fr,),('RH estable')
    else:
        return (Fr,),('RH fuerte')
    
'-----------------------------------------------------------------------------'
def longitudResalto(y,b,m,Q,d,uy,ub,uQ,ud,um):
    """Calcula la longitud del resalto. Círculo, rectángulo, triángulo y trapecial (m=0.5,1 o 2) con ecuaciones empíricas\n
    y = profundidad aguas arriba (m) <br>
    b = base (m) <br>
    Q = caudal (m3/s) <br>
    d = diámetro (m)<br>
    ub = unidades de b (mm, cm, m, in)<br />
    uy = unidades de y (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    ud = unidades de d (mm, cm, m, in)\n
    
    Los parámetros que no se requieran se dejan en 0"""
    
    y=CU_m(y,uy)
    b=CU_m(b,ub)
    d=CU_m(y,ud)
    if uQ=='L':
        Q=Q/1000
    m=CU_theta(m,um)
    m=math.tan(math.radians(m))
    
    Fr=froude(y,b,m,m,"m",Q,0,d,"m","m","m","m3/s")
    if d!=0:
        Lr=y*(11.7*(Fr-1)**0.832)
    elif m==0:
        Lr=y*(9.75*(Fr-1)**1.01)
    elif b==0:
        Lr=y*(4.26*(Fr-1)**0.695)
    else:
        if m==0.5:
            Lr=y*(35*(Fr-1)**0.836)
        elif m==1:
            Lr=y*(23*(Fr-1)**0.885)
        elif m==2:
            Lr=y*(17.6*(Fr-1)**0.905)
    return Lr

'-----------------------------------------------------------------------------'    
def y_asterisco(Q,b,y1,i,ub,uy1,uQ,ui):
    """Calcula y asterisco de secciones rectangulares.\n
    y1 = profundidad aguas arriba (m) <br>
    b = base (m) <br>
    Q = caudal (m3/s) <br>
    i = inclinación del canal (grados, radianes, m/m) <br />
    ub = unidades de b (mm, cm, m, in)<br />
    uy1 = unidades de y1 (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    ui = unidades de inclinacion (mm, cm, m, in)\n
    
    Los parámetros que no se requieran se dejan en 0"""
    
    y1=CU_m(y1,uy1)
    b=CU_m(b,ub)
    if uQ=='L':
        Q=Q/1000
    
    Fr=froude(y1,b,0,Q,0,"m","m","m","m3")
    
    theta=CU_theta(i,ui)
    
    Tau=10**(0.027*theta)
    y=y1/2*(math.sqrt(1+8*Fr**2*Tau**2)-1)
    return y

'-----------------------------------------------------------------------------'
def tipoResalto(Q,b,y,yn,theta,uQ,ub,uy,uyn,ui):
    """Establece de qué tipo de resalto se trata a partir de geometría del canal y la profundidad natural.\n
    y = profundidad aguas arriba (m) <br>
    b = base (m) <br>
    Q = caudal (m3/s) <br>
    yn = profundidad natural aguas abajo (m) <b>
    theta = inclinación del canal (grados, radianes, m/m)
    ub = unidades de b (mm, cm, m, in)<br />
    uy = unidades de y (mm, cm, m, in)<br />
    uyn = unidades de yn (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    ui = unidades de inclinacion (mm, cm, m, in)"""
    
    y=CU_m(y,uy)
    b=CU_m(b,ub)
    yn=CU_m(yn,uyn)
    theta=CU_theta(theta,ui)
    if uQ=='L':
        Q=Q/1000
    
    y2=y_subsecuente(Q,b,0,y,0,"m","m","m3")
    y_a=y_asterisco(Q,b,y,theta,"m","m","m3","grados")
    if y2>yn:
        return (y2,y_a),('tipo A',)
    elif y_a==yn:
        return (y2,y_a),('tipo C',)
    elif y_a>yn:
        return (y2,y_a),('tipo B',)
    elif y_a<yn:
        return (y2,y_a),('tipo D',)
    
'-----------------------------------------------------------------------------'
def ecuacionManning_canal(Q,n,So,m,b,y,kn):    
    ecuacion=n*Q/math.sqrt(So)-kn*(y*b+m*y**2)**(5/3)/(b+2*y*math.sqrt(m**2+1))**(2/3)
    return ecuacion
def derivadaManning_canal(Q,n,So,m,b,y,kn):
    derivada=-(kn*(y*(b+m*y))**(2/3)*(5*b**2+2*b*(3*math.sqrt(m**2+1)+5*m)*y+16*m*math.sqrt(m**2+1)*y**2))/(3*(b+2*math.sqrt(m**2+1)*y)**(5/3))
    return derivada
def ecuacionManning_circ(Q,n,So,y,d,kn):
    ecuacion=n*Q/math.sqrt(So)-kn*((((math.pi+2*math.asin((y-(d/2))/(d/2)))-math.sin(math.pi+2*math.asin((y-(d/2))/(d/2))))*d**2/8)**(5/3))/(((math.pi+2*math.asin((y-(d/2))/(d/2)))*d/2)**(2/3))
    return ecuacion
def derivadaManning_circ(Q,n,So,y,d,kn):
    derivada=-(d**2*kn*(d**2*(-2*math.asin(1-(2*y)/d)-math.sin(2*math.asin(1-(2*y)/d))+math.pi))**(2/3)*(2*math.sin(2*math.asin(1-(2*y)/d))+5*math.pi*math.cos(2*math.asin(1-(2*y)/d))-2*math.asin(1-(2*y)/d)*(5*math.cos(2*math.asin(1-(2*y)/d))+3)+3*math.pi))/(24*2**(1/3)*math.sqrt((y*(d-y))/d**2)*(d*(math.pi-2*math.asin(1-(2*y)/d)))**(5/3))
    return derivada

def yn_manning(Q,n,So,m,b,d,i,uQ,ub,ud,uSo):
    """calcula yn con la ecuación de Manning por medio de Newton-Raphson\n
    Q = caudal (m3/s) <br>
    n = número de Manning <br>
    So = inclinación del canal <br>
    m = inclinación de los lados <br>
    b = base (m) <br>
    d = diámetro (m) <br>
    i = sistema inglés (in) o sistema internacional (si)
    ub = unidades de b (mm, cm, m, in)<br />
    ud = unidades de d (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    uSo = unidades de inclinacion (mm, cm, m, in)"""
    
    d=CU_m(d,ud)
    b=CU_m(b,ub)
    So=CU_theta(So,uSo)
    So=math.tan(math.radians(So))
    if uQ=='L':
        Q=Q/1000
    
    if i.lower()=='in':
        kn=1.49
        
    elif i.lower()=='si':
        kn=1
       
    if d==0:
        error=1
        y=1
        while error>0.0001:
            yn=y-ecuacionManning_canal(Q,n,So,m,b,y,kn)/derivadaManning_canal(Q,n,So,m,b,y,kn)
            error=abs(yn-y)
            y=yn
    else: 
        error=1
        y=1
        while error>0.0001:
            yn=y-ecuacionManning_circ(Q,n,So,y,d,kn)/derivadaManning_circ(Q,n,So,y,d,kn)
            error=abs(yn-y)
            y=yn
    return y
'-----------------------------------------------------------------------------'
    
def pendienteC_limite(n,Q,b,m,d,uQ,ub,ud):
    """Calcula la pendiente crítica a partir de la geometría, el caudal máximo y el n de Manning\n
    n = número de Manning <br>
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    m = inclinación de los lados <br>
    d = diámetro\n
    ub = unidades de b (mm, cm, m, in)<br />
    ud = unidades de d (mm, cm, m, in)<br />
    uQ = unidades de caudal--> L, m3 <br />
    Los parámetros que no sean necesarios se dejan como 0"""
    
    d=CU_m(d,ud)
    b=CU_m(b,ub)
    if uQ=='L':
        Q=Q/1000
    
    
    y = yc(Q,b,m,d,"m","m","m3")
    
    if d == 0:
        A,P,Rh,T,D=geom_r(y,b,m,"m","m")
    else:
        ynd=y/d
        yn,theta,A,P,Rh,T,D=geom_c(d,ynd,"m")
    Sc = Q**2*n**2*P**(4/3)/(A**(10/3))
    return Sc

def pendienteC_especifica(n,m,b,y,d,ub,uy,ud):
    """Calcula la pendiente crítica a partir de la geometría, yc y el n de Manning\n
    n = número de Manning <br>
    yc = profundidad crítica <br>
    b = base (m) <br>
    m = inclinación de los lados <br>
    d = diámetro\n
    ub = unidades de b (mm, cm, m, in)<br />
    ud = unidades de d (mm, cm, m, in)<br />
    uy = unidades de y (mm, cm, m, in) <br />
    Los parámetros que no sean necesarios se dejan como 0"""
    
    d=CU_m(d,ud)
    b=CU_m(b,ub)
    y=CU_m(y,uy)
    
    v=vc(m,b,y,d,"m","m","m")
    if d == 0:
        A,P,Rh,T,D=geom_r(y,b,m,"m","m")
    else:
        ynd=y/d
        yn,theta,A,P,Rh,T,D=geom_c(d,ynd,"m")
    Sc=v**2*n**2/(Rh**(4/3))
    return Sc
'-----------------------------------------------------------------------------'
def funcionIntegral_rectangular(y,Q,n,So,b,m):
    f = ((1-(Q**2*(b+2*m*y))/(9.81*(b*y+m*y**2)**3))/(So-((n**2*Q**2*(b+2*y*math.sqrt(m**2+1))**(4/3))/((b*y+m*y**2)**(10/3)))))
    return f

def funcionIntegral_circular(y,Q,n,So,d):
    theta = np.pi+2*np.arcsin((y-(d/2))/(d/2))
    A= (theta-np.sin(theta))*d**2/8
    P= theta*d/2
    T=2*np.sqrt(y*(d-y))
    
    f=((1-(Q**2*(T))/(9.81*(A)**3))/(So-((n**2*Q**2*(P)**(4/3))/((A)**(10/3)))))
    return f

def fgv_int(Q,n,So,b,m,d,y1,y2,uQ,uSo,ub,ud,uy1,uy2):
    """Calcula la longitud que requiere el flujo para pasar de una profundidad a otra\n
    Q = caudal (m3/s) <br>
    n = número de Manning <br>
    So = Inclinación del canal <br>
    b = base (m) <br>
    m = inclinación de los lados <br>
    d = diámetro (m) <br>
    y1 = profundidad de control (m) <br>
    y2 = profundidad objetivo (m)
    uQ = unidades de caudal--> L, m3 <br />
    uSo = unidades de inclinacion (mm, cm, m, in)
    ub = unidades de b (mm, cm, m, in)<br />
    ud = unidades de d (mm, cm, m, in)<br />
    uy1 = unidades de uy1 (mm, cm, m, in)<br />
    uy2 = unidades de uy2 (mm, cm, m, in)<br />"""
    
    b=CU_m(b,ub)
    d=CU_m(d,ud)
    y1=CU_m(y1,uy1)
    y2=CU_m(y2,uy2)
    So=CU_theta(So,uSo)
    So=math.tan(math.radians(So))
    if uQ=='L':
        Q=Q/1000
    
    
    if d==0:
        x=integrate.quadrature(funcionIntegral_rectangular,y1,y2,args=(Q,n,So,b,m),tol=1e-8)[0]
    else:
        x=integrate.quadrature(funcionIntegral_circular,y1,y2,args=(Q,n,So,d),tol=1e-8)[0] #no cuadra con el resultado de calculadora
    return x

def pasoDirecto(Q,n,So,b,m,d,y1,y2,pasos,datum,uQ,uSo,ub,ud,uy1,uy2):
    """Calcula el perfil de un flujo gradualmente variado a partir de una aproximación de diferencias finitas. Distancia entre dos profundidades conocidas\n
    Q = caudal (m3/s) <br>
    n = número de Manning <br>
    So = Inclinación del canal <br>
    b = base (m) <br>
    m = inclinación de los lados <br>
    d = diámetro (m) <br>
    y1 = profundidad de control (m) <br>
    y2 = profundidad objetivo (m)
    uQ = unidades de caudal--> L, m3 <br />
    uSo = unidades de inclinacion (mm, cm, m, in)
    ub = unidades de b (mm, cm, m, in)<br />
    ud = unidades de d (mm, cm, m, in)<br />
    uy1 = unidades de uy1 (mm, cm, m, in)<br />
    uy2 = unidades de uy2 (mm, cm, m, in)<br />"""
    
    b=CU_m(b,ub)
    d=CU_m(d,ud)
    y_control=CU_m(y1,uy1)
    y_obj=CU_m(y2,uy2)
    So=CU_theta(So,uSo)
    So=math.tan(math.radians(So))
    if uQ=='L':
        Q=Q/1000
    
    
    plot_x=[]
    plot_yc=[]
    plot_yn=[]
    plot_fondo=[]
    plot_y=[]
    
    
    
    
    deltaY=(y_obj-y_control)/pasos
    
    y_c=yc(Q,b,m,0)
    
    if So!=0:
        yn=yn_manning(Q,n,So,m,b,0,'si')
    
    Sc=pendienteC_limite(n,Q,b,m,0)
    
    if So<Sc:
        print ('suave')
    elif So>Sc:
        print ('empinada')
    elif So==Sc:
        print ('crítica')
    elif So==0:
        print ('horizontal')
    elif So<0:
        print ('adversa')
    
    p=0
    y=y_control
    Sfi=0
    Ei=0
    x=0
    fondo=datum
    
    if d==0:
        while p<=pasos:
            A,P,Rh,T,D=geom_r(y, b, m)
            v=Q/A
            E=y+v**2/(2*9.81)
            Sf= Q**2*n**2*P**(4/3)/(A**(10/3))
            if p>0:
                Sfm=(Sf+Sfi)/2
                So_Sfm=So-Sfm
                deltaE=E-Ei
                deltaX=deltaE/So_Sfm
                
                x=x+deltaX
                fondo=datum-x*So
                           
                print (str(p),str("{0:.3f}".format(y)),str("{0:.3f}".format(A)),str("{0:.3f}".format(P)),str("{0:.3f}".format(Rh)),str("{0:.3f}".format(v)),str("{0:.3f}".format(E)),str("{0:.3f}".format(Sf)),str("{0:.3f}".format(Sfm)),str("{0:.3f}".format(So_Sfm)),str("{0:.3f}".format(deltaE)),str("{0:.3f}".format(deltaX)),str("{0:.3f}".format(x)),'\n')
                    
                    
            else:
                print (str(p),str("{0:.3f}".format(y)),str("{0:.3f}".format(A)),str("{0:.3f}".format(P)),str("{0:.3f}".format(Rh)),str("{0:.3f}".format(v)),str("{0:.3f}".format(E)),str("{0:.3f}".format(Sf)),'','','','',str(0),'\n')
           
            plot_x.append(float(x))
            plot_fondo.append(float(fondo))
            plot_y.append(float(y+fondo))
            plot_yc.append(float(y_c+fondo))
            if So!=0:
                plot_yn.append(float(yn+fondo))
                
           
            Sfi=Sf
            Ei=E
            y=y+deltaY
            p=p+1
    print (plot_yn, plot_fondo)