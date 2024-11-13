# depuracion.py
import pandas as pd

def depurar_archivo(file_path):
    """Function to clean and process the uploaded .log file."""
    
    try:
        # Assuming your .log file can be read with Pandas
        # marcaje = pd.read_csv(file_path, header= None, sep=',', usecols=[0, 2, 3, 5, 6], names=["Codigo", "entrada/salida", "rut", "hora", "minuto"])  

        marcaje = pd.read_csv(file_path, header= None, sep=',', 
                      names=["Codigo", "a", "entrada/salida", "rut","b", "hora", "minuto", "día", "mes", "año", "c", "d", "e", "f", "g", "h", "i", "j", "k"])

        # Juntar hora y minuto en una sola columna
        # Antes de exportar archivo en siguiente modulo se dropea col 'Hora' y 'Error'
        marcaje['Hora'] = marcaje['hora'].astype(str).str.zfill(2) + ':' + marcaje['minuto'].astype(str).str.zfill(2)       
        
        
        ruta_reglas = "/app/horarios_mes_actual.csv"
        # names_reglas = ["Codigo", "nombre", "año", "mes", "entrada", "salida", "horaEn", "minutoEn", "horaSal", "minutoSal"]
        reglas = pd.read_csv(ruta_reglas, sep=';').dropna(axis='columns', how='all')
        
    except Exception as e:
            print(f"Error DEPURACION - Crea DF con contenido de archivo subido: {e}")
            return None
    
    ''' DEPURACIONES '''
    
    ''' DUPLICADOS '''
    try:
        marcaje = duplicados(marcaje)
    except Exception as e:
        print(f"Error DEPURACION - proceso DUPLICADOS: {e}")
        return None
    
    ''' FALTA SALIDA'''
    try:
        marcaje = faltaSalida(marcaje, reglas)
    except Exception as e:
        print(f"Error DEPURACION - proceso FALTA SALIDA: {e}")
        return None
    
    ''' MARCA OPUESTO '''
    try:
        marcaje = marcaOpuesto(marcaje, reglas)
    except Exception as e:
        print(f"Error DEPURACION - proceso MARCA OPUESTO: {e}")
        return None
    
    try:
        # Se termina la depuración y se eliminan las columnas que no sirven
        # marcaje = marcaje.drop(columns=['hora', 'minuto']) 

        data = marcaje
        # data = data.dropna()

        # Return processed data or save it to a new file
        # processed_file_path = file_path.replace(".log", "_processed.csv")
        # data.to_csv(processed_file_path, index=False)
        # return processed_file_path  # Return path of processed file

        

        # Save the DataFrame to a CSV file
        path_temp = '/app/temp/datos_procesados.csv'
        data.to_csv(path_temp, index=False, encoding='utf-8')
        print(f"Se guarda archivo procesado en {path_temp}. [Mod Dep]")
        
    
    except Exception as e:
        print(f"Error DEPURACION - proceso GUARDADO ARCHIVO DEPURADO: {e}")
        return None

def duplicados(marcaje):
    entrada = marcaje.copy()  # Crear una copia para evitar modificar el original

    # Ordenar por rut, día y hora
    entrada = entrada.sort_values(by=['rut', 'día', 'Hora']).reset_index(drop=True)

    # Columna de errores
    entrada['Error'] = 'Ok'

    # Verificar entradas duplicadas
    for rut, group in entrada.groupby('rut'):
        
        # Variable para almacenar la última acción
        ultima_accion = None
        for i in range(len(group) - 1):
            fila_actual = group.iloc[i]
            fila_siguiente = group.iloc[i + 1]
            
            # Verificar si hay entradas duplicadas sin salida entre ellas
            if (fila_actual['entrada/salida'] == 1 and fila_siguiente['entrada/salida'] == 1 and ultima_accion != 3):
                # Marcar como entrada duplicada
                entrada.loc[group.index[i + 1], 'Error'] = 'Entrada duplicada'

            # Verificar si hay salidas duplicadas sin entrada entre ellas
            elif (fila_actual['entrada/salida'] == 3 and fila_siguiente['entrada/salida'] == 3 and ultima_accion != 1):
                # Marcar como salida duplicada
                entrada.loc[group.index[i + 1], 'Error'] = 'Salida duplicada'
                
            ultima_accion = fila_actual['entrada/salida']

    entrada = entrada.sort_values(by=['día', 'Hora']).reset_index(drop=True)

    nuevoDf = []

    for i, row in entrada.iterrows():
        # Si no hay error, incluir la fila tal cual
        if row['Error'] == 'Ok':
            nuevoDf.append(row)
            
        elif row['Error'] == 'Entrada duplicada':
            # Agregar la fila actual
            nuevoDf.append(row)

            # Crear una fila de "salida creada por duplicado" con los mismos datos
            salida_row = row.copy()
            salida_row['entrada/salida'] = 3  # Cambiar a salida
            salida_row['Error'] = 'Salida creada por duplicado'
            nuevoDf.append(salida_row)  # Agregar la nueva fila
            
        elif row['Error'] == 'Salida duplicada':
            # Crear una fila de "entrada creada por duplicado" con los mismos datos
            entrada_row = row.copy()
            entrada_row['entrada/salida'] = 1  # Cambiar a entrada
            entrada_row['Error'] = 'Entrada creada por duplicado'
            nuevoDf.append(entrada_row)  # Agregar la nueva fila

            # Agregar la fila actual
            nuevoDf.append(row)

    # Crear un nuevo DataFrame a partir de nuevoDf, que ahora incluye todas las filas
    entrada = pd.DataFrame(nuevoDf)

    return entrada

def faltaSalida(marcaje, reglas):
    salida =  marcaje

    for  i, row in salida.iterrows():

        error = 'Salida automatica detectada'

        if (row['Hora'] == '00:00'):
            if(salida.at[i, 'Error'] == 'Ok'):
                salida.at[i, 'Error'] = error
            else:
                salida.at[i, 'Error'] += f", {error}"

            codigoHorario = row['Codigo']
            
            # Se procede a arreglar reemplazando el horario por el tiempo esperado de salida según reglamento  
            for j, row2 in reglas.iterrows():
                if (codigoHorario == row2['Codigo']):
                    
                    HorarioSalida = row2['salida']
                    horaSalida = row2['horaSal']
                    minutoSalida = row2['minutoSal']

                    break

            salida.at[i, 'hora'] = horaSalida
            salida.at[i, 'minuto'] = minutoSalida
            salida.at[i, 'Hora'] = HorarioSalida      
            salida.at[i, "día"] -= 1    

    salida = salida.sort_values(by=['día', 'Hora']).reset_index(drop=True)
    
    return salida

def marcaOpuesto(marcaje, reglas):
    df = marcaje

    for  i, row in df.iterrows():
        
        codigoHorario = row['Codigo']
        rut = row['rut']

        for j, row2 in reglas.iterrows():
            if (codigoHorario == row2['Codigo']):
                
                horaEntrada = row2['horaEn']
                minutoEntrada = row2['minutoEn']

                horaSalida = row2['horaSal']
                minutoSalida = row2['minutoSal']

                break
        
        # Buscar entrada con una ventanad de 30 minutos en donde se marca salida y corregir
        if (row['hora'] == horaEntrada and (minutoEntrada - 10) <= row['minuto'] and  row['minuto'] <= (minutoEntrada + 30) and rut == row['rut'] and row['entrada/salida'] == 3):
            df.at[i, 'entrada/salida'] = 1
            if (row['Error'] == 'Ok'):
                df.at[i, 'Error'] = "Posible entrada marcada como salida"
            else:
                df.at[i, 'Error'] += ", Posible entrada marcada como salida"

        # Buscar salida con una ventana de 10 minutos en donde se marca entrada y corregir
        if (row['hora'] == horaSalida and (minutoSalida - 10) <= row['minuto'] and  row['minuto'] <= (minutoSalida + 10) and rut == row['rut'] and row['entrada/salida'] == 1):
            df.at[i, 'entrada/salida'] = 3

            if (row['Error'] == 'Ok'):
                df.at[i, 'Error'] = "Posible entrada marcada como salida"
            else:
                df.at[i, 'Error'] += ", Posible entrada marcada como salida"

    return df