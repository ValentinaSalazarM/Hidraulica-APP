# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 22:57:20 2021

@author: JFGJ
"""
from PIL import Image

def tipoPendiente(Tipo):
    
    msg=''
    
    if Tipo == 'Suave':
    
        msg = 'yn > yc'
        
    if Tipo == 'Empinada':
        
        msg = 'yc > yn'
    
    if Tipo == 'Critica':
        
        msg = 'yc = yn'
        
    if Tipo == 'Horizontal':
    
        msg = 'yn = infinito'    
    
    if Tipo == 'Adversa':
        
        msg = 'yn = No existe'
        
    return msg

def abrir_imagen(im):
    
    ruta ='D:/Documents/Hidraulica-APP/Proyecto especial/Flujo gradualmente variado/' + im + '.jfif'
    im = Image.open(ruta)
    im.show()

def tipoZona (Zona):
    
    msg = "Error"
    
    if Zona == 'M1':
        
        abrir_imagen('M1')
        
    elif Zona == 'M2':
    
        abrir_imagen('M2')
    
    elif Zona == 'M3':
    
        abrir_imagen('M3')
    
    
    elif Zona == 'S1':
        
        abrir_imagen('S1')
        
    elif Zona == 'S2':
    
        abrir_imagen('S2')
    
    elif Zona == 'S3':
    
        abrir_imagen('S3')

    elif Zona == 'C1':
        
        abrir_imagen('C1')
        
    elif Zona == 'C2':
    
        abrir_imagen('C2')
    
    elif Zona == 'C3':
    
        abrir_imagen('C3')
    
    elif Zona == 'H1':
        
        msg = 'No existe'
        
    elif Zona == 'H2':
    
        abrir_imagen('H2')
    
    elif Zona == 'H3':
    
        abrir_imagen('H3')  

    
    elif Zona == 'A1':
        
        msg = 'No existe'
       
    elif Zona == 'A2':
    
        abrir_imagen('A2')
    
    elif Zona == 'A3':
    
        abrir_imagen('A3')
        
    return msg

tipoZona('A2')

















































