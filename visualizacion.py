# visualizacion.py
from flask import Flask, render_template, request, session, flash, redirect, Blueprint, current_app
from helpers import user_login_required
import pandas as pd
import os

visualizacion = Blueprint('visualizacion', __name__)

@visualizacion.route('/visualizacion')
@user_login_required
def visualizar():
    """Display the contents of the uploaded CSV file."""
    
    # Verifica que existe el target, El nombre deberia ser el mismo porque se define en carga_archivo
    # y a la copia del archivo que se genera en depuracion.py se le agrega '_processed.csv' (descartando .log)
    
    print('dentro de VIS.py')
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'marcajes_original_processed.csv')
    
    if os.path.exists(file_path):
        # Load the CSV file with pandas
        df = pd.read_csv(file_path)
        # Convert DataFrame to HTML table format
        table_html = df.to_html(classes='table table-striped', index=False)
        return render_template("visualizacion.html", table=table_html)
    else:
        # Handle missing file scenario
        flash("File not found. Please upload a file first.", "error")
        return redirect('/cargar')
