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

# Datos de prueba
@pytest.fixture
def df_corregido():
    data = {
        "Codigo": [1, 2, 3, 4, 5],
        "entrada/salida": [1, 3, 1, 3, 1],
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
    # Verificar que se eliminó la fila con "Salida creada por duplicado"
    assert 1 not in result.index

def test_validar_salida_duplicada(df_corregido):
    selected_rows = pd.DataFrame({
        "Codigo": [2],
        "entrada/salida": [3],
        "rut": ["12345678-9"],
        "hora": ["08"],
        "minuto": ["30"],
        "mes": ["12"],
        "día": [7],
        "año": ["2024"],
        "Error": ["Salida duplicada"],
    })
    result = validar(df_corregido, selected_rows)

    # Depuración: Imprimir DataFrame resultante
    print("DataFrame resultante:")
    print(result)

    # Verificar que "Salida creada por duplicado" no esté presente
    assert not any(result["Error"].str.contains("Salida creada por duplicado"))

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

    # Depuración: Imprimir DataFrame resultante
    print("DataFrame después de validar (Salida automática corregida):")
    print(result)

    # Verificar que el índice 2 no esté presente
    assert 2 not in result.index


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
    # Verificar que el valor en 'entrada/salida' fue cambiado a 3
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
    # Verificar que el valor en 'entrada/salida' fue cambiado a 1
    assert result.at[4, "entrada/salida"] == 1

def test_validar_historial_creado(df_corregido, selected_rows, mocker):
    mock_crear_historial = mocker.patch('validacion.crearHistorial')

    # Ejecutar la función
    result = validar(df_corregido, selected_rows)

    # Verificar que crearHistorial se llamó
    mock_crear_historial.assert_called_once()

    # Validar los parámetros pasados
    called_args = mock_crear_historial.call_args
    print("Parámetros pasados a crearHistorial:", called_args)

    # Verifica DataFrame original y los índices procesados
    assert called_args[0][0].equals(df_corregido)  # DataFrame original
    assert called_args[0][1] == [0]  # Índices esperados

    # Confirmar que los cambios se reflejan
    assert "Correciones revertidas" in result["Error"].values
