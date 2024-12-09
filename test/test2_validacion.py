import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd
from validacion import validar

# Mock para la función crearHistorial
def mock_crearHistorial(df, indices):
    print("Historial creado para los índices:", indices)

# Reemplazar la función original por el mock
import validacion
validacion.crearHistorial = mock_crearHistorial

def cargar_datos_depurados(archivo):
    """
    Carga datos desde un archivo CSV o similar.
    :param archivo: Ruta del archivo con datos.
    :return: DataFrame con los datos cargados.
    """
    return pd.read_csv(archivo)

@pytest.fixture
def df_corregido():
    """
    Carga el archivo de datos procesados para realizar las pruebas.
    """
    archivo = os.path.join("temp", "datos_procesados.csv")  # Ruta relativa al archivo
    return cargar_datos_depurados(archivo)

@pytest.fixture
def selected_rows():
    """
    Fila seleccionada para las pruebas.
    """
    data = {
        "Codigo": [1],
        "entrada/salida": [1],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [7],
        "año": ["2024"],
        "Error": ["Entrada duplicada"],
    }
    return pd.DataFrame(data)

# Tests

def test_validar_entrada_duplicada(df_corregido, selected_rows):
    result = validar(df_corregido, selected_rows)
    assert result is not None
    assert "Entrada duplicada" not in result["Error"].values

def test_validar_salida_automatica_corregida(df_corregido):
    selected_rows = pd.DataFrame({
        "Codigo": [3],
        "entrada/salida": [1],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [8],
        "año": ["2024"],
        "Error": ["Salida automatica corregida"],
    })
    result = validar(df_corregido, selected_rows)
    assert result is not None
    # Verifica que el índice 2 no esté presente en el resultado
    assert 2 not in result.index
    assert "Salida automatica corregida" not in result["Error"].values


def test_validar_salida_invertida_a_entrada(df_corregido):
    selected_rows = pd.DataFrame({
        "Codigo": [4],
        "entrada/salida": [3],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [8],
        "año": ["2024"],
        "Error": ["Salida invertida a entrada"],
    })
    result = validar(df_corregido, selected_rows)
    assert result.at[3, "entrada/salida"] == 3

def test_validar_entrada_invertida_a_salida(df_corregido):
    selected_rows = pd.DataFrame({
        "Codigo": [5],
        "entrada/salida": [1],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [9],
        "año": ["2024"],
        "Error": ["Entrada invertida a salida"],
    })
    result = validar(df_corregido, selected_rows)
    assert result.at[4, "entrada/salida"] == 1

def test_validar_historial_creado(df_corregido, selected_rows, mocker):
    mock_crear_historial = mocker.patch('validacion.crearHistorial')
    result = validar(df_corregido, selected_rows)
    mock_crear_historial.assert_called_once()
