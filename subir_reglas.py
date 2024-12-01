from flask import Flask, render_template, request, session, flash, redirect, Blueprint, current_app
from helpers import admin_login_required
import os
from werkzeug.utils import secure_filename

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
            print(f"New file saved to: {file_path}")
            flash('Archivo subido exitosamente', "success")
            return redirect('/')
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
            flash('Error al subir archivo', "error")
            return render_template("apology.html")
