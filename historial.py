import pandas as pd
from datetime import date

def crearHistorial(df, indices):
    try:
        # Si indices es None, asigna una lista vacía
        if indices is None:
            indices = []

        # Inicializar el DataFrame con columnas
        historial = pd.DataFrame(columns=['usuario', 'rut', 'fecha', 'error', 'cambio'])
        
        # Recuperar usuario de archivo
        temp_path = "/app/temp/username.txt"
        with open(temp_path, "r") as file:
            usuario = file.read()

        

        fecha_actual = date.today().strftime("%d/%m/%Y")  # día/mes/año
  
        for index, row in df.iterrows():
            errores = row['Error']
            correciones = []

            if ((errores != "Ok" and index not in indices) and \
                (errores != "Salida creada por duplicado") and (errores != "Entrada creada por duplicado")):

                lista_errores = errores.split(", ")

                for error in lista_errores:
                    if error == "Entrada duplicada":
                        print("Se reconoce en historial ENTRADA DUPLICADA")
                        correciones.append("Se crea una salida para entrada duplicada")
                    elif error == "Salida duplicada":
                        print("Se reconoce en historial SALIDA DUPLICADA")
                        correciones.append("Se crea una entrada para salida duplicada")
                    elif error == "Salida automatica corregida":
                        print("Se reconoce en historial SALIDA AUTOMATICA")
                        correciones.append(f"Se crea hora de salida según reglas ({row['Hora']})")
                    elif error == "Entrada invertida a salida":
                        print("Se reconoce en historial ENTRADA INVERTIDA A SALIDA")
                        correciones.append("Se invierte marcaje de tipo entrada a marcaje de tipo salida")
    

                
                cambios = f"Se hacen los siguientes cambios: {', '.join(correciones)}"
                rut = row['rut']  # Acceso correcto a la columna 'rut'

                # Crear una nueva fila como DataFrame
                nueva_fila = pd.DataFrame([{
                    'usuario': usuario,
                    'rut': rut,
                    'fecha': fecha_actual,
                    'error': errores,
                    'cambio': cambios
                }])

                # Agregar la nueva fila al historial (sin envolverla en otro pd.DataFrame)
                historial = pd.concat([historial, nueva_fila], ignore_index=True)

            elif (errores == "Salida creada por duplicado" and index - 1 not in indices) or (errores == "Entrada creada por duplicado" and index + 1 not in indices):
                    if errores == "Entrada creada por duplicado":
                        print("Se reconoce en historial ENTRADA CREADA POR DUPLICADO")
                        correciones.append("Entrada creada para corregir salida duplicada")
                    elif errores == "Salida creada por duplicado":
                        print("Se reconoce en historial SALIDA CREADA POR DUPLICADO")
                        correciones.append("Salida creada para corregir entrada duplicada")

                    cambios = f"Se hacen los siguientes cambios: {', '.join(correciones)}"
                    rut = row['rut']  # Acceso correcto a la columna 'rut'

                    # Crear una nueva fila como DataFrame
                    nueva_fila = pd.DataFrame([{
                        'usuario': usuario,
                        'rut': rut,
                        'fecha': fecha_actual,
                        'error': errores,
                        'cambio': cambios
                    }])

                    historial = pd.concat([historial, nueva_fila], ignore_index=True)

        # Guardar el historial en el archivo CSV
        file_path = '/app/temp/historial.csv'

        historial.to_csv(file_path, index=False, header=['usuario', 'rut', 'fecha', 'error', 'cambio'])
        
    except Exception as e:
        print("Error al generar el historial: ", e)
