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
        # Solo carga html 
        return render_template("carga.html")
    else:
        # Comprueba archivo
        if 'file' not in request.files:
            flash('No se detecta archivo', "error")
            return redirect(request.url)
        
        file = request.files['file']
            
        if file.filename == '':
            flash('No se detecta archivo', "error")
            return redirect(request.url)
        
        # Comprobar tambien por extension '.log'
        '''
        if not file.filename.endswith('.log'):
            flash('Tipo de archivo invalido, Intente nuevamente con un archivo tipo .log', "error")
            return redirect(request.url)
        '''
        
        # werkzeug sanitiza nombre archivo
        # filename = secure_filename(file.filename)
        # Recordar cambiar a nombre original (y que sea .log
        filename = 'marcajes_original.csv'

        # Change the file extension to .csv
        # PARA USAR JQuery. pendiente ver si se transforma aqui o en MOD Depuracion
        #csv_filename = filename.replace('.log', '.csv')
        
        # Guarda archivo en file_path 
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print("Se guarda a file_path: ", file_path)

        try:
            file.save(file_path)
        except Exception as e:
            print(f"Error saving file: {e}")
            flash('Error al subir archivo', "error")   
            return render_template("apology.html") # Por ahora
            
        
        # flash('Archivo correctamente importado')
        # Debug
        print(f"File saved to: {file_path}")
        # Para verlo dentro de container
        # docker-compose exec -it flask_app /bin/bash
        # Hacer que sea visible en IDE ??

        
        # EJEMPLO DE MANEJO ARCHIVO
        # Open and process the file from the saved location
        # with open(file_path, 'rb') as f:
            # file_content = f.read()

        # LLama funcion de depuracion principal. Desde esta funcion de manejan varios tipos de depuracion
        #processed_file_path = depurar_archivo(file_path)

        # if processed_filepath:
        if file_path:
                # flash('Archivo depurado correctamente')
                #return redirect('/visualizacion')
                return redirect('/visualizacion')
        else:
            flash('Error en la depuración del archivo', "error")
            return render_template("apology.html")