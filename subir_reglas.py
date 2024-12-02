from flask import Flask, render_template, request, session, flash, redirect, Blueprint, current_app
from helpers import admin_login_required
import os
from werkzeug.utils import secure_filename
from datetime import date
import pandas as pd

subir_reglas = Blueprint('subir_reglas', __name__)

@subir_reglas.route('/subir_reglas', methods=['GET', 'POST'])
@admin_login_required
def carga_reglas_func():
    """Usuario sube archivo de marcajes al sistema"""
    
    if request.method == "GET":
        # Solo carga html 
        return render_template("subir_reglas.html")
    else:
        ''' COMPRUEBA ESTADO DE ARCHIVO '''
        
        # Comprueba archivo
        if 'file' not in request.files:
            flash('No se detecta archivo', "error")
            return redirect('/subir_reglas')
        
        archivo = request.files['file']
        
        if archivo.filename == '':
            flash('No se detecta archivo', "error")
            return redirect('/subir_reglas')
        
        
        ''' MANEJA NOMBRE DEL ARCHIVO SUBIDO'''
        
        # Define the directory to save the file
        upload_dir = '/app/horario_mensual'  # Must match the Docker volume mapping
        os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
        
        # Set the file path with the desired name
        desired_filename = 'horarios_creados.csv'
        file_path = os.path.join(upload_dir, desired_filename)
        
        
        
        ''' elimina horarios anteriormente subidos '''
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Previous file {file_path} deleted successfully.")
            except Exception as e:
                print(f"Error deleting the previous file: {e}")
                flash('Error al eliminar el archivo previo', "error")
                return redirect('/')
        
        ''' Guarda nuevos horarios '''
        try:
            # Save the new file
            archivo.save(file_path)

            # Se procede a depurar las reglas.
            depurarReglas(file_path)

            print(f"New file saved to: {file_path}")
            flash('Archivo subido exitosamente', "success")
            return redirect('/')
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
            flash('Error al subir archivo', "error")
            return render_template("apology.html")

def depurarReglas(file_path):

    # Cargar el archivo
    data = pd.read_csv(file_path, header=None, sep=';', usecols=[1, 3, 5, 7, 15, 16], 
                    names=['Codigo', 'nombre', 'año', 'mes', 'entrada', 'salida'])

    # Para excluir las filas en las que la columna 'Codigo' empiece con "Fecha:"
    data = data[~data['Codigo'].astype(str).str.startswith('Fecha 	:')]

    # Aplicar la función
    data[['horaEn', 'minutoEn']] = data['entrada'].apply(dividir_hora_minuto)
    data[['horaSal', 'minutoSal']] = data['salida'].apply(dividir_hora_minuto)

    # Convertir a enteros, manejando valores NaN (Solo por si acaso, creo que me tiraba error)
    data['horaEn'] = data['horaEn'].fillna(0).astype(int)
    data['minutoEn'] = data['minutoEn'].fillna(0).astype(int)
    data['horaSal'] = data['horaSal'].fillna(0).astype(int)
    data['minutoSal'] = data['minutoSal'].fillna(0).astype(int)

    ''' MOMENTANEAMENTE SE DEJA HARDCODEADA LA FECHA
    # Para obtener la fecha actual (Por si los del hospital nos pasan el horario completo)
    current_date = date.today()
    current_year = current_date.strftime("%Y")
    current_month = current_date.strftime("%m")
    '''

    current_year = "2024"
    current_month = "8"

    # Filtrado por año y mes
    filtered_data = data[(data['año'] == current_year) & (data['mes'] == current_month)]

    # Reset the index if desired
    filtered_data = filtered_data.reset_index(drop=True)

    filtered_data.to_csv(file_path, index=False, encoding='utf-8')

def dividir_hora_minuto(hora_minuto_str):
    # Verificar si el valor es válido
    if isinstance(hora_minuto_str, str) and ':' in hora_minuto_str:
        try:
            hora, minuto = map(int, hora_minuto_str.split(':'))
            return pd.Series([hora, minuto])
        except ValueError:
            return pd.Series([None, None])  # Retornar None si ocurre un error
    else:
        return pd.Series([None, None])  # Retornar None si no es una cadena válida