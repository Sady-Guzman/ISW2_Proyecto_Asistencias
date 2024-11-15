import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import pytest
from depuracion import depurar_archivo, duplicados, faltaSalida, marcaOpuesto  # Importar funciones del módulo

@pytest.fixture
def log_df():
    """Fixture para cargar y estructurar el archivo .log"""
    # Ruta del archivo de ejemplo
    file_path = '../Documentacion/marcajes_08-01-24.log'

    # Definir columnas basadas en el formato del archivo .log
    columns = ["Codigo", "a", "entrada/salida", "rut", "b", "hora", "minuto", "día", "mes", "año", 
               "c", "d", "e", "f", "g", "h", "i", "j", "k"]

    # Crear DataFrame a partir del archivo .log
    log_content = [line.strip().split(',') for line in open(file_path, 'r', encoding='utf-8')]
    df = pd.DataFrame(log_content, columns=columns)

    # Convertir columnas relevantes a tipos numéricos
    df["hora"] = df["hora"].astype(int)
    df["minuto"] = df["minuto"].astype(int)
    df["día"] = df["día"].astype(int)
    df["mes"] = df["mes"].astype(int)
    df["año"] = df["año"].astype(int)
    df["entrada/salida"] = df["entrada/salida"].astype(int)

    return df

@pytest.fixture
def reglas(log_df):
    """Fixture para generar el DataFrame de reglas de prueba"""
    return pd.DataFrame({
        "Codigo": log_df['Codigo'].unique(),
        "horaEn": [8] * len(log_df['Codigo'].unique()),
        "minutoEn": [0] * len(log_df['Codigo'].unique()),
        "horaSal": [18] * len(log_df['Codigo'].unique()),
        "minutoSal": [0] * len(log_df['Codigo'].unique())
    })

def test_pdd_001(log_df):
    """Prueba de detección de duplicados."""
    result = duplicados(log_df)
    duplicados_detectados = result[result['Error'] == 'Entrada duplicada']
    assert not duplicados_detectados.empty, "Error en la detección de duplicados"

def test_pdd_002(log_df):
    """Prueba de manejo de duplicados múltiples."""
    result = duplicados(log_df)
    duplicados_detectados = result[result['Error'] == 'Entrada duplicada']
    assert duplicados_detectados.shape[0] > 1, "Error en la detección de duplicados múltiples"

def test_pdd_003(log_df, reglas):
    """Prueba de identificación de omisión de salida."""
    result = faltaSalida(log_df, reglas)
    omision_salida = result[result['Error'] == 'Salida automatica corregida']
    assert not omision_salida.empty, "Error en la corrección de omisión de salida"

def test_pdd_004(log_df, reglas):
    """Prueba de identificación de omisión de entrada."""
    result = faltaSalida(log_df, reglas)
    omision_entrada = result[result['Error'] == 'Omisión de entrada']
    assert not omision_entrada.empty, "Error en la identificación de omisión de entrada"

def test_pdd_005(log_df, reglas):
    """Prueba de corrección automática de acción opuesta."""
    result = marcaOpuesto(log_df, reglas)
    accion_opuesta = result[result['Error'] == 'Salida invertida a entrada']
    assert not accion_opuesta.empty, "Error en la corrección de acción opuesta"

def test_pdd_006(log_df):
    """Prueba de rendimiento con gran volumen de datos."""
    result = depurar_archivo(log_df)
    assert result is not None, "Error en el procesamiento de gran volumen de datos"

# Para ejecutar el archivo, utiliza el comando:
# pytest test_depuracion.py
