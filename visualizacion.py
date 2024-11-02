# # visualizacion.py
# from flask import Flask, render_template, request, session, flash, redirect, Blueprint, current_app
# from helpers import user_login_required
# import pandas as pd
# import os

# visualizacion = Blueprint('visualizacion', __name__)

# @visualizacion.route('/visualizacion')
# @user_login_required
# def visualizar():
#     """Display the contents of the uploaded CSV file."""
    
#     # Verifica que existe el target, El nombre deberia ser el mismo porque se define en carga_archivo
#     # y a la copia del archivo que se genera en depuracion.py se le agrega '_processed.csv' (descartando .log)
    
#     print('dentro de VIS.py')
    
#     file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'marcajes_original_processed.csv')
    
#     if os.path.exists(file_path):
#         # Load the CSV file with pandas
#         df = pd.read_csv(file_path)
#         # Convert DataFrame to HTML table format
#         table_html = df.to_html(classes='table table-striped', index=False)
#         return render_template("visualizacion.html", table=table_html)
#     else:
#         # Handle missing file scenario
#         flash("File not found. Please upload a file first.", "error")
#         return redirect('/cargar')

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
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'marcajes_original_processed.csv')
    
    if os.path.exists(file_path):
        # Load the CSV file with pandas
        df = pd.read_csv(file_path)
        
        # Prepare data for rendering in Jinja2 template
        table_columns = df.columns.tolist()  # List of column names
        table_data = df.values.tolist()  # List of rows as lists
        
        return render_template("visualizacion.html", table_columns=table_columns, table_data=table_data)
    else:
        # Handle missing file scenario
        flash("File not found. Please upload a file first.", "error")
        return redirect('/cargar')

@visualizacion.route('/apply_filters', methods=['POST'])
@user_login_required
def apply_filters():
    """Apply filters to the displayed data."""

    # Get filter values from the form
    rut_filter = request.form.get('rut_filter')
    from_hour = request.form.get('from_hour')
    to_hour = request.form.get('to_hour')
    tipo_marcaje = request.form.get('tipo_marcaje')
    condicion = request.form.get('condicion')

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'marcajes_original_processed.csv')
    
    if os.path.exists(file_path):
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
        
        # Prepare data for rendering in Jinja2 template
        table_columns = df.columns.tolist()
        table_data = df.values.tolist()
        
        # Render the filtered data back to the visualization page
        return render_template("visualizacion.html", table_columns=table_columns, table_data=table_data)
    else:
        flash("File not found. Please upload a file first.", "error")
        return redirect('/cargar')

