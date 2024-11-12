# depuracion.py
import pandas as pd

def depurar_archivo(file_path):
    """Function to clean and process the uploaded .log file."""
    try:
        '''
        # Assuming your .log file can be read with Pandas
        # marcaje = pd.read_csv(file_path, header= None, sep=',', usecols=[0, 2, 3, 5, 6], names=["Codigo", "entrada/salida", "rut", "hora", "minuto"])  

        marcaje = pd.read_csv("marcajes_08-01-24.log", header= None, sep=',', 
                      names=["Codigo", "a", "entrada/salida", "rut","b", "hora", "minuto", "día", "mes", "año", "c", "d", "e", "f", "g", "h", "i", "j", "k"])

        # Juntar hora y minuto en una solo columna
        marcaje['Hora'] = marcaje['hora'].astype(str).str.zfill(2) + ':' + marcaje['minuto'].astype(str).str.zfill(2)       

        reglas = pd.read_csv('Horarios Mes actual.csv')

        # Depuración
        marcaje = duplicados(marcaje)
        marcaje = faltaSalida(marcaje, reglas)
        marcaje = marcaOpuesto(marcaje, reglas)

        # Se termina la depuración y se eliminan las columnas que no sirven
        # marcaje = marcaje.drop(columns=['hora', 'minuto']) 

        data = marcaje
        data = data.dropna()
        # Return processed data or save it to a new file
        processed_file_path = file_path.replace(".log", "_processed.csv")
        data.to_csv(processed_file_path, index=False)
        return processed_file_path  # Return path of processed file

        '''

        # Path to the log file
        # log_file = 'path_to_log_file.log'
        #log_file = '/app/temp/marcajes_original.log'
        log_file = '/app/temp/marcajes_original.log'

        # Read the log file into a pandas DataFrame assuming it's comma-separated
        df = pd.read_csv(log_file, header=None, encoding='utf-8')
        # Assign the new column names as per your desired output
        df.columns = ['codigo', 'entrada_salida', 'rut', 'hora', 'minuto', 'mes', 'dia', 'anho', 'accion']

        # Save the DataFrame to a CSV file
        df.to_csv('/app/temp/datos_procesados.csv', index=False, encoding='utf-8')
        
        processed_file_path = '/app/temp/datos_procesados.csv'

        # Optionally, print the DataFrame to verify
        # print(df.head())
        return processed_file_path  # Return path of processed file
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def duplicados(marcaje):
    entrada = marcaje

    # Ordenar por rut día y hora
    entrada = entrada.sort_values(by=['rut', 'día', 'Hora']).reset_index(drop=True)

    # Columna de errores
    entrada['Error'] = 'Ok'

    # Verficar entrada (1) - entrada (1) sin salida (3) en medio
    for rut, group in entrada.groupby('rut'):
        
        # Cual fue la ultima accion
        ultima_accion = None
        for i in range(len(group) - 1):
            fila_actual = group.iloc[i]
            fila_siguiente = group.iloc[i + 1]
            
            # Revisa si no existe ninguna entrada duplicada
            if (fila_actual['entrada/salida'] == 1 and fila_siguiente['entrada/salida'] == 1 and ultima_accion != 3):

                # Marcar entrada duplicada
                entrada.loc[group.index[i + 1], 'Error'] = 'Entrada duplicada'

            elif (fila_actual['entrada/salida'] == 3 and fila_siguiente['entrada/salida'] == 3 and ultima_accion != 1):
                
                # Marcar salida duplicada
                entrada.loc[group.index[i + 1], 'Error'] = 'Salida duplicada'
                
            
            ultima_accion = fila_actual['entrada/salida']

            
    entrada = entrada.sort_values(by=['día', 'Hora']).reset_index(drop=True)

    nuevoDf = []

    for i, row in entrada.iterrows():
              
            if row['Error'] == 'Entrada duplicada':

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
            for j, row2 in reglas.itrrows():
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

        for j, row2 in reglas.itrrows():
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