# visualizacion.py
from flask import render_template, flash, redirect, Blueprint, current_app
from helpers import user_login_required
import pandas as pd
import os

visualizacion = Blueprint('visualizacion', __name__)

@visualizacion.route('/visualizacion')
@user_login_required
def visualizar():
    """Display the contents of the uploaded CSV file."""

    
    # Path al archivo a mostrar (Archivo ya paso por depuracion)
    file_path = '/app/temp/datos_procesados.csv'
    
    
    
    if os.path.exists(file_path):
        # Load the CSV file with pandas
        df = pd.read_csv(file_path)

        # Prepare data for rendering in the template
        table_columns = df.columns.tolist()
        table_data = df.values.tolist()
        
        return render_template("visualizacion.html", table_columns=table_columns, table_data=table_data)
    else:
        flash("Archivo no disponible. Por favor importar archivo.", "error")
        return redirect('/cargar')

    

''' FUNC DE FILTROS PENDIENTE'''

''' Version en desarrollo '''

@visualizacion.route('/apply_filters', methods=['POST'])
@user_login_required
def apply_filters():
    """Apply filters to the displayed data."""
    from flask import request  # Import request module to get form data

    # Get filter values from the form
    rut_filter = request.form.get('rut_filter')
    from_hour = request.form.get('from_hour')
    to_hour = request.form.get('to_hour')
    tipo_marcaje = request.form.get('tipo_marcaje')
    condicion = request.form.get('condicion')

    file_path = '/app/temp/datos_procesados.csv'
    
    # Filtros estan en desarrollo. No aplica en MAIN BRANCH
    if 1 == 1:
        flash("La función de filtro aún está en construcción.", "error")
        return render_template("apology.html")
    else:
        try:
            # Load the CSV file with pandas
            df = pd.read_csv(file_path)
            
            # Apply filters if they are provided
            if rut_filter:
                df = df[df['rut'] == rut_filter]
            
            if from_hour and to_hour:
                df = df[(df['hora'] >= from_hour) & (df['hora'] <= to_hour)]
            
            if tipo_marcaje != 'any':
                df = df[df['marcaje'] == tipo_marcaje]
            
            if condicion != 'any':
                df = df[df['condicion'] == condicion]
            
            # Prepare data for rendering in the template
            table_columns = df.columns.tolist()
            table_data = df.values.tolist()
            
            # Render the filtered data back to the visualization page
            return render_template("visualizacion.html", table_columns=table_columns, table_data=table_data)
        
        except Exception as e:
            flash("La función de filtro aún está en construcción.", "error")
            return render_template("apology.html")
