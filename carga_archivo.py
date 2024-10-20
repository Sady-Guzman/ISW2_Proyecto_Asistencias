from flask import Flask, render_template, request, session, flash, redirect, Blueprint, current_app
from helpers import user_login_required
import os
from werkzeug.utils import secure_filename


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
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
            
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Comprobar tambien por extension '.log' y contenido tabular
        
        # werkzeug sanitiza nombre archivo
        filename = secure_filename(file.filename)
        
        # Guarda archivo
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('Archivo correctamente importado')
        
        # Debug
        print(f"File saved to: {file_path}")
        # Para verlo dentro de container
        # docker-compose exec -it flask_app /bin/bash
        # Hacer que sea visible en IDE ??

        
        # EJEMPLO DE MANEJO ARCHIVO
        # Open and process the file from the saved location
        with open(file_path, 'rb') as f:
            file_content = f.read()

        # Redirigir a siguiente modulo 'depuracion'
        # TODO

        # render  siguiente modulo 'visualizar.html'. TODO
        return render_template("apology.html") # Por ahora