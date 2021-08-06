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
'Funciones que retornan geometría del canal'

def  geom_c(d,ynd):
    """ Esta función retorna la geometría de un canal circular\n
    d=diametro(m)<br />
    ynd=relación de llenado"""
    yn=ynd*d
    theta = math.pi+2*math.asin((yn-(d/2))/(d/2))
    A= (theta-math.sin(theta))*d**2/8
    P= theta*d/2
    Rh=(1-math.sin(theta)/theta)*d/4
    T=d*math.cos(math.asin((yn-(d/2))/(d/2)))
    D=A/T
    return yn,theta,A,P,Rh,T,D

def geom_r(y,b,m):
    """ Esta función retorna la geometría de un canal geométrico no circular\n
    y=profundidad (m)<br />
    b=base (m)<br />
    m=inclinación"""
    A = b*y+m*y**2
    P=b+2*y*math.sqrt(m**2+1)
    Rh=A/P
    T=b+2*m*y
    D=A/T
    return A,P,Rh,T,D

'-----------------------------------------------------------------------------'
def froude(y,b,m,Q,d):
    """Calcula el número de froude con las propiedades geométricas y el caudal\n
    y=profundidad (m)<br />
    b=base (m)<br />
    m=inclinación <br />
    Q=caudal (m3/s) <br />
    d=diámetro<br />
    Los parámetros que no se requieran, se dejan en 0"""
    
    if d==0:
        A,P,Rh,T,D=geom_r(y,b,m)
    else:
        ynd=y/d
        yn,theta,A,P,Rh,T,D=geom_c(d,ynd)
    
    Fr=Q/(A*math.sqrt(9.81*A/T))
    return Fr

'-----------------------------------------------------------------------------'
def ecuacion_yc_Rectangulo(Q,b,m,y):
    ecuacion=((Q/math.sqrt(9.81))-(m*y**2+b*y)*math.sqrt(m*y**2+b*y)/(math.sqrt(2*m*y+b)))
    return ecuacion

def derivada_yc_Rectangulo(Q,b,m,y):
    derivada=-(10*m**2*y**2+10*b*m*y+3*b**2)*math.sqrt(m*y**2+b*y)/(2*(2*m*y+b)**(3/2))
    return derivada

def ecuacion_yc_Circulo(Q,d,y):
    ecuacion=(Q/math.sqrt(9.81))-((((d**2)/8)*(math.pi+2*math.asin((y-(d/2))/(d/2))-math.sin(math.pi+2*math.asin((y-(d/2))/(d/2)))))**(3/2)/(d*math.sin((math.pi+2*math.asin((y-(d/2))/(d/2)))/2))**(1/2))
    return ecuacion

def derivada_yc_Circulo(Q,d,y):
    derivada=((d**2*(2*math.asin((2*(y-d/2))/d)+math.sin(2*math.asin((2*(y-d/2))/d))+math.pi))**(3/2)*math.cos(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi)))/(16*math.sqrt(2)*math.sqrt(1-(4*(y-d/2)**2)/d**2)*(d*math.sin(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi)))**(3/2))-(3*d**2*math.sqrt(d**2*(2*math.asin((2*(y-d/2))/d)+math.sin(2*math.asin((2*(y-d/2))/d))+math.pi))*(4/(d*math.sqrt(1-(4*(y-d/2)**2)/d**2))+(4*math.cos(2*math.asin((2*(y-d/2))/d)))/(d*math.sqrt(1-(4*(y-d/2)**2)/d**2))))/(32*math.sqrt(2)*math.sqrt(d*math.sin(1/2*(2*math.asin((2*(y-d/2))/d)+math.pi))))        
    return derivada

def yc(Q,b,m,d):  
    """Calcula la profundidad crítica. Para secciones rectángulares se recurre a una solución analítica. Para las demás se recurre a una solución numérica (Newton-Raphson)\n
    Q = caudal (m3/s) <br />
    b = base (m) <br />
    m = inclinación <br />
    d = diámetro (m) \n    
     Los parámetros que no se requieran, se dejan en 0"""
    if d==0:        
        if m==0:
            yc=((Q**2)/(9.81*(b**2)))**(1/3)
        else:
            error=1
            y=b
            
            while error>0.0001:
                yc=y-ecuacion_yc_Rectangulo(Q,b,m,y)/derivada_yc_Rectangulo(Q,b,m,y)
                error=abs(yc-y)
                y=yc
    else:
        error=1
        y=d/2
        while error>0.0001:
            yc=y-ecuacion_yc_Circulo(Q,d,y)/derivada_yc_Circulo(Q,d,y)
            error=abs(yc-y)
            y=yc

    return float(yc)

'-----------------------------------------------------------------------------'
def vc (m,b,y,d):
    """Calcula la velocidad crítica a partir de Froude y geometría crítica\n
    m = inclinación de lados <br>
    b = base (m) <br>
    y = profundidad crítica (m) <br>
    d = diámetro (m) \n
    Los parámetros que no sean necesarios se dejan en 0"""
    if d==0:
        A,P,Rh,T,D = geom_r(y,b,m)
    else:
        ynd=y/d
        yn,theta,A,P,Rh,T,D=geom_c(d,ynd)
    
    v=math.sqrt(9.81*A/T)
    return v
    
'-----------------------------------------------------------------------------'
def momentum(Q,b,m,y,d):
    """Calcula momentum de una sección a partir de geometría y caudal\n
    Q = caudal (m3/s) <br />
    b = base (m) <br />
    m = inclinación <br />
    d = diámetro (m)"""    
    if d==0:        
        if m==0:
            mom=y**2/2+(Q/b)**2/(9.81*y)
            
        elif b==0:
            mom=m*y**3/3+Q**2/(9.81*m*y**2)
        else:
            mom=m*y**3/3+b*y**2/2+Q**2/(9.81*(m*y**2+b*y))
    
    else:
        theta = math.pi+2*math.asin((y-(d/2))/(d/2))
        mom=d**3/24*(3*math.sin(theta/2)-(math.sin(theta/2))**3-3*(theta/2)*math.cos(theta/2))+Q**2/(9.81*d**2*(theta-math.sin(theta))/8)
    return float(mom)

'-----------------------------------------------------------------------------'
'    Falta probar los no rectangulares'

def fuerzaCompuerta(y1,y2,b,Q,m,rho):
    """Calcula fuerza sobre la compuerta en canales primáticos\n
    y1= profundidad de sección 1 <br />
    y2= profundidad de sección 2 <br />
    b = base (m) <br />
    Q = caudal (m3/s) <br />
    m = inclinación <br />
    rho = densidad (kg/m3)"""

    M1=momentum(Q,b,m,y1,0)
    M2=momentum(Q,b,m,y2,0)
    
    if m==0:
        f=rho*9.81*b*(M1-M2)
    else:
        f=rho*9.81*(M1-M2)
    return M1,M2,f


'-----------------------------------------------------------------------------'
def ecuacionTriangulo(Q,m,y1,y2,f):
    ecuacion= ((1/3)*(y1**3-y2**3)+(Q**2/(9.81*m)*((1/y1**2)-(1/y2**2)))-f)/(y2-y1)
    return ecuacion
def derivadaTriangulo(Q,m,y1,y2,f):
    derivada=((2*Q**2)/(9.81*m*y2**3)-y2**2)/(y2-y1)-(-f+(Q**2*(1/y1**2-1/y2**2))/(9.81*m)+1/3*(y1**3-y2**3))/(y2-y1)**2
    return derivada


def ecuacionTrapecio(Q,m,b,y1,y2,f):
    ecuacion=((m/3)*(y1**3-y2**3)+(b/2)*(y1**2-y2**2)+(Q**2/9.81)*((1/(m*y1**2+b*y1))-(1/(m*y2**2+b*y2)))-f)/(y2-y1)
    return ecuacion 
def derivadaTrapecio(Q,b,m,y1,y2,f):
    derivada=((Q**2*(b+2*m*y2))/(9.81*(b*y2+m*y2**2)**2)-b*y2-m*y2**2)/(y2-y1)-((Q**2*(1/(b*y1+m*y1**2)-1/(b*y2+m*y2**2)))/9.81+(1/2)*b*(y1**2-y2**2)+1/3*m*(y1**3-y2**3)-f)/(y2-y1)**2
    return derivada


def y_subsecuente(Q,b,m,y1,f):
    """Calcula profundidad subsecuente por medio de conservación del momento. Para canales rectangulares se utiliza la solución analítica. Para los demás se recurre a una solución numérica (Newton Raphson).\n
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    y1 = profundidad de sección 1 <br>
    f=fuerza aplicada en caso de resalto forzado (si no es forzado, poner 0)"""
    
    if m==0:
        Fr=froude(y1,b,m,Q,0,0)
        y2=y1/2*(math.sqrt(1+8*Fr**2)-1)
    elif b==0:
        error=1
        y=2*y1
        while error>0.0001:
            y2=y-ecuacionTriangulo(Q,m,y1,y,f)/derivadaTriangulo(Q,m,y1,y,f)
            error=abs(y2-y)
            y=y2
    else:
        error=1
        y=2*y1
        while error>0.0001:
            y2=y-ecuacionTrapecio(Q,m,b,y1,y,f)/derivadaTrapecio(Q,b,m,y1,y,f)
            error=abs(y2-y)
            y=y2
    return y2

'-----------------------------------------------------------------------------'
def eficienciaRH(Q,b,m,y1,f):
    """Calcula eficiencia del RH a partir del caudal, geometría aguas arriba y fuerza en caso de ser forzado\n
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    y1 = profundidad en sección 1 <br>
    f = fuerza aplicada en caso de resalto forzado (si no es forzado, poner 0)"""
    
    y2=y_subsecuente(Q, b, m, y1,f)
    
    A1,P1,Rh1,T1,D1=geom_r(y1,b,m)
    A2,P2,Rh2,T2,D2=geom_r(y2,b,m)
        
    E1=y1+Q**2/(2*9.81*A1**2)
    E2=y2+Q**2/(2*9.81*A2**2)+f
    
    eficiencia=abs(E1-E2)/E1*100
    
    return eficiencia

'-----------------------------------------------------------------------------'
def eficienciaRHI(Q,b,m,y1,yn,l,theta):
    """Calcula eficiencia del RH inclinado a partir del caudal, geometría aguas arriba, inclinación del canal y longitud de la parte inclinada del canal (utilizar gráfica)\n
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    y1 = profundidad en sección 1 <br>
    l = longitud de la parte inclinada del resalto (m) <br>
    theta = inclinación del canal en grados"""
    z=l*math.tan(math.radians(theta))
    A1,P1,Rh1,T1,D1=geom_r(y1,b,m)
    A2,P2,Rh2,T2,D2=geom_r(yn,b,m)

    E1=y1+Q**2/(2*9.81*A1**2)+z
    E2=yn+Q**2/(2*9.81*A2**2)
    
    eficiencia=abs(E1-E2)/E1*100
    
    return eficiencia
'-----------------------------------------------------------------------------'
def clasificacionResalto(Q,b,m,y):
    """Clasifica resalto con el número de Froude a partir de las propiedades geométricas aguas arriba\n
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    m = inclinación <br>
    y = profundidad aguas arriba"""
    A,P,Rh,T,D=geom_r(y,b,m)
    Fr=froude(y,b,m,Q,0,0)
    if Fr<1:
        return 'Flujo subcrítico'
    elif Fr<=1.7:
        return 'RH ondular'
    elif Fr<=2.5:
        return 'RH débil'
    elif Fr<=4.5:
        return 'RH oscilante'
    elif Fr<=9:
        return 'RH estable'
    else:
        return 'RH fuerte'
    
'-----------------------------------------------------------------------------'
def longitudResalto(y,b,m,Q,d):
    """Calcula la longitud del resalto. Círculo, rectángulo, triángulo y trapecial (m=0.5,1 o 2)\n
    y = profundidad aguas arriba (m) <br>
    b = base (m) <br>
    Q = caudal (m3/s) <br>
    d = diámetro (m)\n
    
    Los parámetros que no se requieran se dejan en 0"""
    
    Fr=froude(y,b,m,Q,d)
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
def y_asterisco(Q,b,y1,theta):
    """Calcula y asterisco de secciones rectangulares.\n
    y1 = profundidad aguas arriba (m) <br>
    b = base (m) <br>
    Q = caudal (m3/s) <br>
    theta = inclinación del canal en grados"""
    Fr=froude(y1,b,0,Q,0,0)
    Tau=10**(0.027*theta)
    y=y1/2*(math.sqrt(1+8*Fr**2*Tau**2)-1)
    return y

'-----------------------------------------------------------------------------'
def tipoResalto(Q,b,y,yn,theta):
    """Establece de qué tipo de resalto se trata a partir de geometría del canal y la profundidad natural.\n
    y = profundidad aguas arriba (m) <br>
    b = base (m) <br>
    Q = caudal (m3/s) <br>
    yn = profundidad natural aguas abajo (m) <b>
    theta = inclinación del canal en grados"""
    
    y2=y_subsecuente(Q,b,0,y,0)
    y_a=y_asterisco(Q,b,y,theta)
    if y2>yn:
        return 'tipo A'
    elif y_a==yn:
        return 'tipo C'
    elif y_a>yn:
        return 'tipo B'
    elif y_a<yn:
        return 'tipo D'
    
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

def yn_manning(Q,n,So,m,b,d,i):
    """calcula yn con la ecuación de Manning por medio de Newton-Raphson\n
    Q = caudal (m3/s) <br>
    n = número de Manning <br>
    So = inclinación del canal <br>
    m = inclinación de los lados <br>
    b = base (m) <br>
    d = diámetro (m) <br>
    i = sistema inglés (in) o sistema internacional (si)"""
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
    
def pendienteC_limite(n,Q,b,m,d):
    """Calcula la pendiente crítica a partir de la geometría, el caudal máximo y el n de Manning\n
    n = número de Manning <br>
    Q = caudal (m3/s) <br>
    b = base (m) <br>
    m = inclinación de los lados <br>
    d = diámetro\n
    Los parámetros que no sean necesarios se dejan como 0"""
    
    y = yc(Q,b,m,d)
    
    if d == 0:
        A,P,Rh,T,D=geom_r(y,b,m)
    else:
        ynd=y/d
        yn,theta,A,P,Rh,T,D=geom_c(d,ynd)
    Sc = Q**2*n**2*P**(4/3)/(A**(10/3))
    return Sc

def pendienteC_especifica(n,m,b,y,d):
    """Calcula la pendiente crítica a partir de la geometría, yc y el n de Manning\n
    n = número de Manning <br>
    yc = profundidad crítica <br>
    b = base (m) <br>
    m = inclinación de los lados <br>
    d = diámetro\n
    Los parámetros que no sean necesarios se dejan como 0"""
    v=vc(m,b,y,d)
    if d == 0:
        A,P,Rh,T,D=geom_r(y,b,m)
    else:
        ynd=y/d
        yn,theta,A,P,Rh,T,D=geom_c(d,ynd)
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

def fgv_int(Q,n,So,b,m,d,y1,y2):
    """Calcula la longitud que requiere el flujo para pasar de una profundidad a otra\n
    Q = caudal (m3/s) <br>
    n = número de Manning <br>
    So = Inclinación del canal <br>
    b = base (m) <br>
    m = inclinación de los lados <br>
    d = diámetro (m) <br>
    y1 = profundidad de control (m) <br>
    y2 = profundidad objetivo (m)"""
    
    if d==0:
        x=integrate.quadrature(funcionIntegral_rectangular,y1,y2,args=(Q,n,So,b,m),tol=1e-8)[0]
    else:
        x=integrate.quadrature(funcionIntegral_circular,y1,y2,args=(Q,n,So,d),tol=1e-8)[0] #no cuadra con el resultado de calculadora
    return x

def pasoDirecto(Q,n,So,b,m,d,y_control,y_obj,pasos,datum):
    """Calcula el perfil de un flujo gradualmente variado a partir de una aproximación de diferencias finitas. Distancia entre dos profundidades conocidas\n
    Q = caudal (m3/s) <br>
    n = número de Manning <br>
    So = Inclinación del canal <br>
    b = base (m) <br>
    m = inclinación de los lados <br>
    d = diámetro (m) <br>
    y1 = profundidad de control (m) <br>
    y2 = profundidad objetivo (m)"""
    
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
        
        





#algoritmoSeleccionado = sys.argv[1]

#if algoritmoSeleccionado.lower() == 'geometria':
#    print("Esta función retorna las propiedades geométricas de la tubería o canal!")
 #   geometria ()
#elif algoritmoSeleccionado.lower() == 'f':
#    print("Esta función calcula la fuerza aplicada sobre una compuerta de flujo inferior a partir de conservación del momentum!")
#    fuerzaCompuerta()