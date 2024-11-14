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
        
        # Seleccionar solo las cols que tienen info relevante.
        # El archivo que generan los relojes tiene varios campos que no se usan.
        # 0: Codigo, 2: Entrada(1)/Salida(3), 3: RUT, 5: Hora, 6: Minuto, 7: Mes, 8: Dia, 9: Anho, 21: Estado/Error/Solucion
        df_filtrado = df.iloc[:, [0, 2, 3, 5, 6, 7, 8, 9, 20]]

        # Prepare data for rendering in the template
        table_columns = df_filtrado.columns.tolist()
        table_data = df_filtrado.values.tolist()
        
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
    codigo_filter = request.form.get('codigo_filter')

    file_path = '/app/temp/datos_procesados.csv'
    
    # Filtros estan en desarrollo. No aplica en MAIN BRANCH
    try:
        # Load the CSV file with pandas
        df = pd.read_csv(file_path)
        

        # FILTRO RUT
        if rut_filter:
            df = df[df['rut'] == rut_filter]
        
        # Filtro TIEMPO --- Falta arreglar formato 12 y 24 horas
        # Combina las columnas hora y minuto
        df['time'] = pd.to_datetime(df['hora'].astype(str) + ':' + df['minuto'].astype(str), format='%H:%M').dt.time
        
        # Aplica los filtros independientemente entre to y from
        if from_hour:
            from_hour = pd.to_datetime(from_hour, format='%H:%M').time()
            df = df[df['time'] >= from_hour]
        
        if to_hour:
            to_hour = pd.to_datetime(to_hour, format='%H:%M').time()
            df = df[df['time'] <= to_hour]

        
        # Filtro por ENTRADA / SALIDA
        # if tipo_marcaje:

        #     # Asigna el numero correspondiente a el marcaje para filtrar en df
        #     if tipo_marcaje == "Entrada":
        #         tipo_numerico = "01"
        #     if tipo_marcaje == "Salida":
        #         tipo_numerico = "03"

        #     # Compara con codigo numerico
        #     df = df[df['entrada/salida'] == tipo_numerico]


        # Filtro por ENTRADA / SALIDA
        if tipo_marcaje and tipo_marcaje != 'any':
            # Map 'Entrada' to '01' and 'Salida' to '03'
            # Ojo con codigo, Deberia tener 0 a la izquierda
            
            if tipo_marcaje == "entrada":
                tipo_numerico = "1"
            else:
                tipo_numerico = "3"
            

            print(f"El tipo de marcaje que se busca es: {tipo_marcaje}, y tipo_numerico: {tipo_numerico}")

            try:
                # Ensure that the column is treated as a string to match "01" or "03"
                df['entrada/salida'] = df['entrada/salida'].astype(str)
                
                # Apply the filter based on `tipo_numerico`
                df = df[df['entrada/salida'] == tipo_numerico]
            except Exception as e:
                print(f"Error filtering entrada/salida: {e}")
                flash("Error al filtrar por entrada/salida.", "error")
                return render_template("apology.html")
        

        # Filtro por ESTADO del marcaje
        # Puede ser OK, DUPLICADO, SALTADO, OPUESTO
        if condicion and condicion != 'any':

            print("Valor de variable condicion: ", condicion)

            # Define keywords based on the selected condition
            keywords = []
            if condicion == "duplicado":
                keywords = ["duplicado", "duplicada"]
            elif condicion == "saltado":
                keywords = ["automatica"]
            elif condicion == "invertir":
                keywords = ["invertida"]
            elif condicion == "correcto":
                print("Se elige Correcto en filtro")
                keywords = ["Ok"]

            print(" Pasa Keywords")

            # Debug: Print the filtered DataFrame to confirm
            # print(df.head())
            
            # If there are keywords to filter, apply the filter
            if keywords:
                # Combine the keywords into a regex pattern (e.g., 'duplicado|duplicada')
                pattern = '|'.join(keywords)

                # Debug: Print the pattern for confirmation
                print("Pattern:", pattern)


                try:
                    # Check the 'error' column first for any NaN values, strip whitespaces, and apply filter
                    df['Error'] = df['Error'].str.strip()  # Remove leading/trailing spaces
                except Exception as e: 
                    print(f"Error str.strip condicion: {e}")
                    return render_template("apology.html")
                try:
                     # Filter rows where 'error' contains any of the keywords as substrings
                    df = df[df['Error'].str.contains(pattern, case=False, na=False)]

                except Exception as e: 
                    print(f"Error filtering condicion: {e}")
                    return render_template("apology.html")


                # Debug: Print the filtered DataFrame to confirm
                print(df.head())

            else:
                print("No keywords to filter on.")
                
        
        
        # FILTRO codigo
        if codigo_filter:
            print("Codigo ingresado: ", codigo_filter)
            print(df['Codigo'].head())

            # Convert 'Codigo' column to string for comparison
            df['Codigo'] = df['Codigo'].astype(str)
            df = df[df['Codigo'] == codigo_filter]
        


        ''' Saca columnas 'basura' de df que se muestra en MOD VIS '''


        # Seleccionar solo las cols que tienen info relevante.
        # El archivo que generan los relojes tiene varios campos que no se usan.
        # 0: Codigo, 2: Entrada(1)/Salida(3), 3: RUT, 5: Hora, 6: Minuto, 7: Mes, 8: Dia, 9: Anho, 21: Estado/Error/Solucion
        df_filtrado = df.iloc[:, [0, 2, 3, 5, 6, 7, 8, 9, 20]]
        
        # Prepare data for rendering in the template
        table_columns = df_filtrado.columns.tolist()
        table_data = df_filtrado.values.tolist()
        
        # Render the filtered data back to the visualization page
        return render_template("visualizacion.html", table_columns=table_columns, table_data=table_data)
    
    except Exception as e:
        print(f"Error: {e}")        
        flash("La función de filtro aún está en construcción.", "error")
        return render_template("apology.html")
