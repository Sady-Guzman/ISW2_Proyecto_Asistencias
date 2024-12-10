# depuracion.py
import pandas as pd

def depurar_archivo(file_path):
    """Function to clean and process the uploaded .log file."""
    
    try:
        # Se carga el archivo en la carpeta temp

        marcaje = pd.read_csv(file_path, header= None, sep=',', 
                      names=["Codigo", "a", "entrada/salida", "rut","b", "hora", "minuto", "mes", "día", "año", "c", "d", "e", "f", "g", "h", "i", "j", "k"], 
                      dtype={"Codigo": str,"a": str,"entrada/salida": str,"b": str,"c": str,"d": str,"e": str,"f": str,"g": str,"h": str,"i": str,"j": str,"k": str})

        # Juntar hora y minuto en una sola columna
        marcaje['Hora'] = marcaje['hora'].astype(str).str.zfill(2) + ':' + marcaje['minuto'].astype(str).str.zfill(2)       
        
        try:
            ruta_reglas = "/app/horario_mensual/horarios_creados.csv"
            reglas = pd.read_csv(ruta_reglas, sep=',').dropna(axis='columns', how='all')
        except Exception as e:
            print(f"Error al cargar archivo de reglas {e}")
            return None
        
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

    ''' REVISION DE SALIDAS '''
    try:
        marcaje['cierre'] = "No tiene cierre"
        marcaje = marcaje.sort_values(by=['rut', 'día', 'Hora']).reset_index(drop=True)
        
        for indice in range(len(marcaje.index)):
            if marcaje.at[indice, 'entrada/salida'] == "01":
                registraSalida(marcaje, indice)
        
        marcaje = marcaje.sort_values(by=['día', 'Hora', 'rut']).reset_index(drop=True)
           
    except Exception as e:
        print(f"Error DEPURACION - proceso TIENE SALIDA: {e}")
        return None
    
    ''' FALTA SALIDA '''
    try:
        marcaje = faltaSalida(marcaje, reglas)
        marcaje = marcaje.sort_values(by=['día', 'Hora', 'rut']).reset_index(drop=True)
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
        
        data = marcaje

        # Guardar DataFrame en CSV en la carpeta temp
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
            
            # Verificar si hay entradas duplicadas sin salida entre ellas y son el mismo día
            if (fila_actual['entrada/salida'] == "01" and fila_siguiente['entrada/salida'] == "01" and ultima_accion != "03" and 
                fila_actual['día'] == fila_siguiente['día']):
                # Marcar como entrada duplicada
                entrada.loc[group.index[i + 1], 'Error'] = 'Entrada duplicada'

            # Verificar si hay salidas duplicadas sin entrada entre ellas y son el mismo día
            elif (fila_actual['entrada/salida'] == 3 and fila_siguiente['entrada/salida'] == 3 and ultima_accion != "01" and 
                  fila_actual['día'] == fila_siguiente['día']):
                # Marcar como salida duplicada
                entrada.loc[group.index[i + 1], 'Error'] = 'Salida duplicada'
                
            ultima_accion = fila_actual['entrada/salida']

    entrada = entrada.sort_values(by=['día', 'Hora', 'rut']).reset_index(drop=True)

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
            salida_row['entrada/salida'] = "03"  # Cambiar a salida
            salida_row['Error'] = 'Salida creada por duplicado'
            nuevoDf.append(salida_row)  # Agregar la nueva fila
            
        elif row['Error'] == 'Salida duplicada':
            # Crear una fila de "entrada creada por duplicado" con los mismos datos
            entrada_row = row.copy()
            entrada_row['entrada/salida'] = "01"  # Cambiar a entrada
            entrada_row['Error'] = 'Entrada creada por duplicado'
            nuevoDf.append(entrada_row)  # Agregar la nueva fila

            # Agregar la fila actual
            nuevoDf.append(row)

    # Crear un nuevo DataFrame a partir de nuevoDf, que ahora incluye todas las filas
    entrada = pd.DataFrame(nuevoDf)

    return entrada

def registraSalida(marcaje, indice):
    # Obtener la fila actual
    fila = marcaje.iloc[indice]

    # Buscar posibles salidas válidas después de esta entrada
    posibles_salidas = marcaje[
        (marcaje['rut'] == fila['rut']) & 
        (marcaje['día'] == fila['día']) & 
        (marcaje['entrada/salida'] == "03") & 
        (marcaje.index > indice)
    ]

    if not posibles_salidas.empty:
        # Tomar la primera salida encontrada
        salida_index = posibles_salidas.index[0]
        
        # Marcar tanto la entrada como la salida
        marcaje.at[indice, 'cierre'] = "Tiene cierre"
        marcaje.at[salida_index, 'cierre'] = "Tiene cierre"

        # Llamada recursiva para buscar un cierre adicional desde la fila de salida
        registraSalida(marcaje, salida_index)
    
    return



def faltaSalida(marcaje, reglas):
    salida = marcaje.copy()

    for i, row in salida.iterrows():

        error = 'Salida automatica corregida'

        # Si el registro es una entrada y no tiene salida
        if row['entrada/salida'] == "01" and row['cierre'] == "No tiene cierre":
            
            codigoHorario = int(row['Codigo'])
            
            # Buscar el horario correspondiente en reglas
            regla = reglas[reglas['Codigo'] == codigoHorario]
            if not regla.empty:
                HorarioSalida = regla.iloc[0]['salida']
                horaSalida = regla.iloc[0]['horaSal']
                minutoSalida = regla.iloc[0]['minutoSal']

                # Si la hora de salida por regla es mayor que la hora actual de la fila (sale el mismo día)
                if horaSalida > row['hora'] or (horaSalida == row['hora'] and minutoSalida > row['minuto']):
                    # Actualizar fila que no tiene cierre
                    salida.at[i, 'cierre'] = "Tiene cierre"

                    # Crear nueva fila y añadirla al DataFrame
                    nueva_fila = row.copy()
                    nueva_fila['entrada/salida'] = "03"
                    nueva_fila['hora'] = horaSalida
                    nueva_fila['minuto'] = minutoSalida
                    nueva_fila['Hora'] = HorarioSalida         
                    nueva_fila['Error'] = error
                    nueva_fila['cierre'] = "Tiene cierre"

                    salida = pd.concat([salida, pd.DataFrame([nueva_fila])], ignore_index=True)

    # Ordenar el DataFrame por día y hora
    salida = salida.sort_values(by=['día', 'Hora', 'rut']).reset_index(drop=True)
    
    return salida


def marcaOpuesto(marcaje, reglas):
    df = marcaje.copy()

    for  i, row in df.iterrows():
        
        codigoHorario = int(row['Codigo'])
        rut = row['rut']

        for j, row2 in reglas.iterrows():
            if (codigoHorario == row2['Codigo']):
                
                horaSalida = row2['horaSal']
                minutoSalida = row2['minutoSal']

                break
            
        # Buscar salida con una ventana de 10 minutos en donde se marca entrada y corregir
        if (row['hora'] == horaSalida and (minutoSalida - 10) <= row['minuto'] and  row['minuto'] <= (minutoSalida + 10) and rut == row['rut'] 
            and row['entrada/salida'] == "01" and row['Error'] == "Ok" and row['cierre'] != "Tiene cierre"):

            df.at[i, 'entrada/salida'] = "03"

            if (row['Error'] == 'Ok'):
                df.at[i, 'Error'] = "Entrada invertida a salida"
            else:
                df.at[i, 'Error'] += ", Entrada invertida a salida"

    return df