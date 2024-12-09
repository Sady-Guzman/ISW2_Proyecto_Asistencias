import sys
import os

# Agregar el directorio raíz (/app) al PYTHONPATH
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

@pytest.fixture
def df_corregido():
    """
    DataFrame de ejemplo para pruebas.
    """
    data = {
        "Codigo": [1, 2, 3, 4, 5],
        "entrada/salida": ["01", "03", "01", "03", "01"],
        "rut": ["12345678-9"] * 5,
        "hora": ["08"] * 5,
        "minuto": ["30"] * 5,
        "mes": ["12"] * 5,
        "día": [7, 7, 8, 8, 9],
        "año": ["2024"] * 5,
        "Error": [
            "Entrada duplicada",
            "Salida creada por duplicado",
            "Salida automatica corregida",
            "Salida invertida a entrada",
            "Entrada invertida a salida",
        ],
    }
    return pd.DataFrame(data)

@pytest.fixture
def selected_rows():
    """
    Fila seleccionada para pruebas.
    """
    data = {
        "Codigo": [1],
        "entrada/salida": ["01"],
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
    """
    Verifica que las filas duplicadas de entrada se eliminen correctamente.
    """
    result = validar(df_corregido, selected_rows)
    assert 1 not in result.index
    assert "Salida creada por duplicado" not in result["Error"].values

def test_validar_salida_duplicada(df_corregido):
    """
    Verifica que las filas duplicadas de salida se eliminen correctamente.
    """
    selected_rows = pd.DataFrame({
        "Codigo": [2],
        "entrada/salida": ["03"],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [7],
        "año": ["2024"],
        "Error": ["Salida duplicada"],
    })
    result = validar(df_corregido, selected_rows)
    assert "Salida creada por duplicado" not in result["Error"].values

def test_validar_salida_automatica_corregida(df_corregido):
    """
    Verifica que las salidas automáticas corregidas se eliminen correctamente.
    """
    selected_rows = pd.DataFrame({
        "Codigo": [3],
        "entrada/salida": ["01"],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [8],
        "año": ["2024"],
        "Error": ["Salida automatica corregida"],
    })
    result = validar(df_corregido, selected_rows)
    assert 2 not in result.index

def test_validar_salida_invertida_a_entrada(df_corregido):
    """
    Verifica que las salidas invertidas a entradas sean corregidas correctamente.
    """
    selected_rows = pd.DataFrame({
        "Codigo": [4],
        "entrada/salida": ["03"],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [8],
        "año": ["2024"],
        "Error": ["Salida invertida a entrada"],
    })
    result = validar(df_corregido, selected_rows)
    assert result.at[3, "entrada/salida"] == "03"

def test_validar_entrada_invertida_a_salida(df_corregido):
    """
    Verifica que las entradas invertidas a salidas sean corregidas correctamente.
    """
    selected_rows = pd.DataFrame({
        "Codigo": [5],
        "entrada/salida": ["01"],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [9],
        "año": ["2024"],
        "Error": ["Entrada invertida a salida"],
    })
    result = validar(df_corregido, selected_rows)
    assert result.at[4, "entrada/salida"] == "01"

def test_validar_historial_creado(df_corregido, selected_rows, mocker):
    """
    Verifica que el historial de correcciones se genere correctamente.
    """
    mock_crear_historial = mocker.patch('validacion.crearHistorial')
    result = validar(df_corregido, selected_rows)
    mock_crear_historial.assert_called_once()
    called_args = mock_crear_historial.call_args
    assert called_args[0][0].equals(df_corregido)
    assert called_args[0][1] == [0]
    assert "Correcciones revertidas" in result["Error"].values