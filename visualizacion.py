# visualizacion.py
from flask import render_template, flash, redirect, Blueprint, current_app, send_file, request
from helpers import user_login_required
import pandas as pd
import os
from validacion import validar
from datetime import date
import json
from historial import crearHistorial

visualizacion = Blueprint('visualizacion', __name__)

@visualizacion.route('/visualizacion')
@user_login_required
def visualizar():
    """Mostrar los contenidos del csv cargado."""

    
    # Path al archivo a mostrar (Archivo ya paso por depuracion)
    file_path = '/app/temp/datos_procesados.csv'
    
    
    
    if os.path.exists(file_path):
        # Cargar CSV 
        df = pd.read_csv(file_path, dtype={'Codigo': str, "entrada/salida": str})
        
        # Seleccionar solo las cols que tienen info relevante.
        # El archivo que generan los relojes tiene varios campos que no se usan.
        # 0: Codigo, 2: Entrada(1)/Salida(3), 3: RUT, 5: Hora, 6: Minuto, 7: Mes, 8: Dia, 9: Anho, 20: Estado/Error/Solucion
        df_filtrado = df.iloc[:, [0, 2, 3, 5, 6, 7, 8, 9, 20]]

        # Preparar los datos para el rendering en el template
        table_columns = df_filtrado.columns.tolist()
        table_data = df_filtrado.values.tolist()
        
        #  Obtener todos los días distintos para el filtrado de días
        df['día'] = df['día'].astype(str)  # Días deben ser string
        distinct_days = sorted(df['día'].unique())  # Se ordenan los días
        
        return render_template("visualizacion.html", table_columns=table_columns, table_data=table_data, distinct_days=distinct_days)
    else:
        flash("Archivo no disponible. Por favor importar archivo.", "error")
        return redirect('/cargar')

    


@visualizacion.route('/apply_filters', methods=['POST'])
@user_login_required
def apply_filters():
    """Aplicar filtros a los datos mostrados"""
    from flask import request  # Importar el módulo request

    # Obtener los filtros seleccionados del form
    rut_filter = request.form.get('rut_filter')
    from_hour = request.form.get('from_hour')
    to_hour = request.form.get('to_hour')
    tipo_marcaje = request.form.get('tipo_marcaje')
    condicion = request.form.get('condicion')
    codigo_filter = request.form.get('codigo_filter')
    day_filter = request.form.getlist('day_filter')


    file_path = '/app/temp/datos_procesados.csv'
    
    # Filtros estan en desarrollo. No aplica en MAIN BRANCH
    try:
        # Cargar CSV con pandas
        df = pd.read_csv(file_path, dtype={'Codigo': str, "entrada/salida": str})
        
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
        if tipo_marcaje and tipo_marcaje != 'any':
            # Map 'Entrada' a '01' y 'Salida' a '03'
            
            if tipo_marcaje == "entrada":
                tipo_numerico = "01"
            else:
                tipo_numerico = "03"
            

            print(f"El tipo de marcaje que se busca es: {tipo_marcaje}, y tipo_numerico: {tipo_numerico}")

            try:
                # Columna debe ser tratada como string por registros "01" o "03" (entrada, salida respectivamente)
                df['entrada/salida'] = df['entrada/salida'].astype(str)
                
                # Aplicar el filtro basado en `tipo_numerico`
                df = df[df['entrada/salida'] == tipo_numerico]
            except Exception as e:
                print(f"Error filtrando entrada/salida: {e}")
                flash("Error al filtrar por entrada/salida.", "error")
                return render_template("apology.html")
        

        # Filtro por ESTADO del marcaje
        # Puede ser OK, DUPLICADO, SALTADO, OPUESTO
        if condicion and condicion != 'any':

            print("Valor de variable condicion: ", condicion)

            # Definir keywords basadas en la selección
            keywords = []
            if condicion == "duplicado":
                keywords = ["duplicado", "duplicada"]
            elif condicion == "saltado":
                keywords = ["automatica"]
            elif condicion == "invertir":
                keywords = ["invertida"]
            elif condicion == "problema":
                keywords = ["duplicado", "duplicada", "invertida", "automatica"]
            elif condicion == "correcto":
                # print("Se elige Correcto en filtro")
                keywords = ["Ok"]

            # print(" Pasa Keywords")

            # Debug: Print el dataframe filtrado para revisar
            # print(df.head())
            
            # Si hay keywords (errores) seleccionadas se filtra
            if keywords:
                # Combinar las keywords en un patron
                pattern = '|'.join(keywords)

                # Debug: Print el patron para revisar
                print("Pattern:", pattern)


                try:
                    # Revisar si las columnas de 'error' primero por algún valor NaN, eliminar espacio en blanco, y aplicar filtro
                    df['Error'] = df['Error'].str.strip()  # Eliminar espacios
                except Exception as e: 
                    print(f"Error str.strip condicion: {e}")
                    return render_template("apology.html")
                try:
                     # Filtrar filas donde 'error' alguna de los substrings de keywords
                    df = df[df['Error'].str.contains(pattern, case=False, na=False)]

                except Exception as e: 
                    print(f"Error filtrando condicion: {e}")
                    return render_template("apology.html")


                # Debug: Print el dataframe filtrado para revisar
                print(df.head())

            else:
                print("No hay errores seleccionados")
                
        
        
        # FILTRO codigo
        if codigo_filter:
            print("Codigo ingresado: ", codigo_filter)
            print(df['Codigo'].head())

            # Converitr 'Código' como string para comparar
            df['Codigo'] = df['Codigo'].astype(str)
            df = df[df['Codigo'] == codigo_filter]

        
        # Obtener todos los días distintos para el filtrado
        df['día'] = df['día'].astype(str)  # La columna 'día' debe ser string
        distinct_days = sorted(df['día'].unique())  # Ordenar los días
        
        # Aplicar el filtro de 'día' si fue seleccionado
        if day_filter:
            print("Días filtrados:", day_filter)
            try:
                # La columna 'día' debe ser string
                df['día'] = df['día'].astype(str)
                # Filtrar los días que coincidan con los días seleccionados
                df = df[df['día'].isin(day_filter)]
            except Exception as e:
                print(f"Error en el filtrado de días: {e}")
                flash("Error al filtrar por días.", "error")
                return render_template("apology.html")
        


        ''' Saca columnas 'basura' de df que se muestra en MOD VIS '''


        # Seleccionar solo las cols que tienen info relevante.
        # El archivo que generan los relojes tiene varios campos que no se usan.
        # 0: Codigo, 2: Entrada(1)/Salida(3), 3: RUT, 5: Hora, 6: Minuto, 7: Mes, 8: Dia, 9: Anho, 21: Estado/Error/Solucion
        df_filtrado = df.iloc[:, [0, 2, 3, 5, 6, 7, 8, 9, 20]]
        
        # Se preparan los datos para el render
        table_columns = df_filtrado.columns.tolist()
        table_data = df_filtrado.values.tolist()
        
        # Carga los datos filtrados en la página de visualizacion
        return render_template("visualizacion.html", table_columns=table_columns, table_data=table_data, distinct_days=distinct_days, enumerate=enumerate)
    
    except Exception as e:
        print(f"Error: {e}")        
        flash("La función de filtro aún está en construcción.", "error")
        return render_template("apology.html")


# FUNCION DE EXPORTAR DATAFRAME COMO CSV A HOST.
# Usa send_file de Flask
@visualizacion.route('/download_csv', methods=['GET', 'POST'])
@user_login_required
def download_csv():

    # Recuperar filas seleccionadas como JSON
    selected_rows = request.form.getlist('selected_rows')

    file_path = '/app/temp/datos_procesados.csv'
    df = pd.read_csv(file_path, dtype={"Codigo": str,"a": str, "entrada/salida": str, "b": str,"c": str,"d": str,"e": str,"f": str,"g": str,"h": str,"i": str,"j": str,"k": str})
    
    if not selected_rows:

        try:          
            df_final = df.copy()
            df_final.drop(columns=['Hora', 'Error', 'cierre'], inplace=True)
            df_final['hora'] = df_final['hora'].apply(lambda x: f"{x:02}")
            df_final['minuto'] = df_final['minuto'].apply(lambda x: f"{x:02}")
            df_final['mes'] = df_final['mes'].apply(lambda x: f"{x:02}")
            df_final['día'] = df_final['día'].apply(lambda x: f"{x:02}")
            df_final['año'] = df_final['año'].apply(lambda x: f"{x:02}")

            crearHistorial(df, None)

            # Guardar dataframe a csv
            df_final.to_csv(file_path, index=False, header=False)

            # Enviar documento para descargar
            return send_file(file_path, 
                            as_attachment=True, 
                            download_name="filtered_data.csv",
                            mimetype='text/csv')

        except Exception as e:
            print(f"Error while generating CSV: {e}")
            flash("Error al generar el archivo CSV.", "error")
            return redirect('/visualizacion')

    else:
        try:
            # Convertir las filas seleccionadas en DataFrame
            columnas = ["Codigo", "entrada/salida", "rut", "hora", "minuto", "mes", "día", "año", "Error"]
            
            try:
                selected_rows = [json.loads(row) for row in selected_rows]
                print("FILAS SELECCIONADAS\n", selected_rows)
            except Exception as e:
                print("Error al cargar Filas: ", e)
                
            df_selected = pd.DataFrame(selected_rows, columns=columnas)

            # Convertir la columna 'día' a tipo entero
            df_selected["día"] = df_selected["día"].astype(int)

            df_final = validar(df, df_selected)

            df_final = df_final.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]]

            # Guardar DataFrame como un CSV
            df_final.to_csv(file_path, index=False, header=False)

            # Enviar documento para descargar 
            return send_file(file_path, 
                            as_attachment=True, 
                            download_name="filtered_data.csv",
                            mimetype='text/csv')

        except Exception as e:
            print(f"Error al generar el archivo CSV: {e}")
            flash("Error al generar el archivo CSV.", "error")
            return redirect('/visualizacion')

        

@visualizacion.route('/download_historial', methods=['GET'])
def download_historial():
    try:
        file_path = '/app/temp/historial.csv'
        fecha_actual = date.today().strftime("%d_%m_%Y")  # día_mes_año
        nombre = f"Historial_{fecha_actual}.csv" # Crear el nombre del archivo 

        return send_file(file_path, as_attachment=True, download_name=nombre)
    except Exception as e:
        print(f"Error: {e}")
        flash("Error al descargar el historial.", "error")
        return redirect('/visualizacion')
    
