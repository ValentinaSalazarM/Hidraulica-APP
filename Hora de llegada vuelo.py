def calcular_horario_llegada(hora_salida: int, minuto_salida: int, segundo_salida: int, duracion_horas: int, duracion_minutos: int, duracion_segundos: int)->str:
    
    """ Hora de llegada de vuelo
    Parámetros:
      hora_salida (int): Hora de salida del vuelo (valor entre 0 y 23)
      minuto_salida (int): Minuto de salida del vuelo (valor entre 0 y 59)
      segundo_salida (int): Segundo de salida del vuelo (valor entre 0 y 59)
      duracion_horas (int): Número de horas que dura el vuelo
      duracion_minutos (int): Número de minutos (adicionales al número de horas) que dura el vuelo
      duracion_segundos (int): Número de segundos (adicionales al número de horas y minutos) que dura el
                               vuelo
    Retorno:
      str: Cadena que indica la hora de llegada del vuelo a su destino, la cadena debe estar con el formato
           “HH:mm:ss”.
    """
    hora_llegada = hora_salida + duracion_horas
    minuto_llegada = minuto_salida + duracion_minutos
    segundo_llegada = segundo_salida + duracion_segundos

    
    if segundo_llegada >= 60:
      minuto_llegada += 1
      segundo_llegada -= 60

    if minuto_llegada >= 60:
      hora_llegada += 1
      minuto_llegada -= 60

    if hora_llegada >= 24:
      diferencia = hora_llegada - 24
      hora_llegada = diferencia

    respuesta = str(hora_llegada) + ':' + str(minuto_llegada) + ':' + str(segundo_llegada)

    return respuesta

print(calcular_horario_llegada(23, 30, 0, 0, 40, 20))

print (calcular_horario_llegada(21, 30, 0, 1, 31, 20))

