# historial.py
import pandas as pd
from datetime import date

def crearHistorial(rut, lista_errores):

    # Inicializar el DataFrame con columnas
    historial = pd.DataFrame(columns=['usuario', 'rut', 'fecha', 'cambio'])
    fecha_actual = date.today().strftime("%d/%m/%Y")  # día/mes/año

    # Recuperar usuario de archivo
    temp_path = "/app/temp/username.txt"
    with open(temp_path, "r") as file:
        usuario = file.read()

    # Crear el cambio como texto
    cambios = f"Se revierte lo siguiente: {', '.join(lista_errores)}, marcaje de: {rut}"

    # Crear una nueva fila como DataFrame
    nueva_fila = pd.DataFrame([{
        'usuario': usuario,
        'rut': rut,
        'fecha': fecha_actual,
        'cambio': cambios
    }])

    # Concatenar con el historial existente
    historial = pd.concat([historial, nueva_fila], ignore_index=True)

    return historial


def guardarHistorial(historial):
    
    file_path = '/app/temp/historial.csv'

    historial.to_csv(file_path, index=False, header=False)