from flask import Flask, render_template, request, session, flash, redirect, Blueprint, current_app
from helpers import user_login_required
import os
from werkzeug.utils import secure_filename
from depuracion import depurar_archivo  # funcion de depuracion de depuracion.py. Redirige a varios pasos de depuracion distintos
from visualizacion import visualizar # Busca y muestra archivo

carga_archivo = Blueprint('carga_archivo', __name__)

@carga_archivo.route('/cargar', methods=['GET', 'POST'])
@user_login_required
def carga_archivo_func():
    """Usuario sube archivo de marcajes al sistema"""
    
    if request.method == "GET":
        # Solo carga template html 
        return render_template("carga.html")
    else:
        
        ''' COMPRUEBA ESTADO DE ARCHIVO '''
        
        # Comprueba archivo
        if 'file' not in request.files:
            flash('No se detecta archivo', "error")
            return redirect('/cargar')
        
        # Asigna nombre alias para manejar paquete
        archivo = request.files['file']
        
            
        if archivo.filename == '':
            flash('No se detecta archivo', "error")
            return redirect('/cargar')
        
        # Comprobar por extension, TIENE QUE SER '.log'
        # Archivo que se obtiene de reloj de marcaje del hospital son siempre .log
        # Agregar tipos de extension o sacar esta comprobacion en caso de cambiar tipo reloj
        
        if not archivo.filename.endswith('.log'):
            flash('Tipo de archivo invalido, Intente nuevamente con un archivo tipo .log', "error")
            return redirect(request.url)

        
        ''' MANEJA NOMBRE DEL ARCHIVO SUBIDO'''
        
        # Filename es solo el NOMBRE
        filename = archivo.filename
        
        # Siempre se usa el mismo nombre para el archivo durante el manejo y se guarda el nombre original en un archivo txt
        # En /app/temp/...
        with open("/app/temp/NOMBRE_ORIGINAL_ARCHIVO.txt", "w") as file:
           file.write(filename)
        filename = 'marcajes_original.log'


        ''' TRANSFORMA Y GUARDA ARCHIVO EN CONTAINER '''
        
        # Durante la depuracion y la visualizacion, se maneja el archivo de marcajes como CSV
        # En el paso final de exportacion (Descarga) se le asigna extension .log
        
        # CSV_FILENAME en vez de modificar original
        csv_filename = filename.replace('.log', '.csv')
        
        
        # Guarda archivo en file_path 
        # cambiar 'csv_filename' por 'filename' despues de debug
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], csv_filename)
        # '/app/temp/"filename que se le asigna" '

        try:
            archivo.save(file_path)
            print("Se guarda archivo correctamente")
            print(f"File saved to: {file_path}")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")
            flash('Error al subir archivo', "error")   
            return render_template("apology.html") # Por ahora
        
        
        ''' Para ver archivo dentro de container'''
        # docker-compose exec -it flask_app /bin/bash
        # Directorio es temp
        # cd temp        
        
        ''' Pasa a fase de depuracion '''
        
        # LLama funcion de depuracion principal. Desde esta funcion de manejan varios tipos de depuracion. No esta en esta branch
        depurar_archivo(file_path)
        
        # if processed_filepath:
        if file_path:
                return redirect('/visualizacion')
        else:
            flash('Error en la depuración del archivo', "error")
            return render_template("apology.html")