import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from validacion import validar


# Función auxiliar para comparar DataFrames y simplificar las pruebas
def assert_frame_equal(df1, df2):
    pd.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True))

# Función para verificar la existencia del archivo 'datos_procesados.csv'
def verificar_archivo():
    archivo = 'temp/datos_procesados.csv'
    if not os.path.exists(archivo):
        print(f"Error: El archivo {archivo} no se encuentra en la ubicación esperada.")
        # Aquí podrías crear el archivo o tomar una acción alternativa
        # Para las pruebas, podrías crear un archivo vacío de prueba
        df = pd.DataFrame(columns=["Codigo", "entrada/salida", "rut", "hora", "minuto", "mes", "día", "año", "Error"])
        df.to_csv(archivo, index=False)
    else:
        # Lógica para continuar con el procesamiento del archivo
        pass

# Casos de prueba

def test_reversion_salida_duplicada():
    # PVD-001
    df = pd.read_csv('./datos_procesados.csv')  # Asegúrate de que la ruta sea correcta
    expected_data = {
        "Codigo": [1],
        "entrada/salida": [1],
        "rut": ["123"],
        "hora": [8],
        "minuto": [0],
        "mes": [1],
        "día": [1],
        "año": [2024],
        "Error": ["Ok"]
    }
    expected_df = pd.DataFrame(expected_data)

    result = validar(df, df)  # Asegúrate de que df esté definido
    assert_frame_equal(result, expected_df)

def test_reversion_entrada_duplicada():
    # PVD-002
    df = pd.read_csv('./datos_procesados.csv')  # Asegúrate de que la ruta sea correcta
    expected_data = {
        "Codigo": [2],
        "entrada/salida": [1],
        "rut": ["123"],
        "hora": [9],
        "minuto": [0],
        "mes": [1],
        "día": [1],
        "año": [2024],
        "Error": ["Ok"]
    }
    expected_df = pd.DataFrame(expected_data)

    result = validar(df, df)
    assert_frame_equal(result, expected_df)

def test_correccion_entrada_invertida_a_salida():
    # PVD-003
    df = pd.read_csv('./datos_procesados.csv')  # Asegúrate de que la ruta sea correcta
    expected_data = {
        "Codigo": [3],
        "entrada/salida": [1],
        "rut": ["123"],
        "hora": [8],
        "minuto": [0],
        "mes": [1],
        "día": [1],
        "año": [2024],
        "Error": ["Correcciones revertidas"]
    }
    expected_df = pd.DataFrame(expected_data)

    result = validar(df, df)
    assert_frame_equal(result, expected_df)

def test_validacion_sin_errores():
    # PVD-007
    df = pd.read_csv('./datos_procesados.csv')  # Asegúrate de que la ruta sea correcta
    expected_df = df[df['Error'] == "Ok"]

    result = validar(df, df)
    assert_frame_equal(result, expected_df)

def test_manejo_de_errores_ejecucion():
    # PVD-010
    try:
        df = pd.read_csv('./datos_procesados.csv')  # Asegúrate de que la ruta sea correcta
        # Simula un error en el proceso
        validar(df, None)  # Pasar un parámetro inválido para provocar un error
    except Exception as e:
        assert "Error en el proceso de corrección" in str(e)
