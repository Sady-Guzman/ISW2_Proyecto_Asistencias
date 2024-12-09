import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pandas as pd
from unittest.mock import mock_open, patch
from io import StringIO
from datetime import date
from historial import crearHistorial  # Asume que el código está en un archivo llamado crear_historial.py

@pytest.fixture
def mock_data():
    data = {
        "rut": ["12345678-9", "98765432-1", "56789012-3"],
        "Error": ["Entrada duplicada", "Ok", "Salida invertida a entrada"],
        "Hora": ["08:00", "12:00", "18:00"]
    }
    return pd.DataFrame(data)

def test_crear_historial(mock_data):
    # Mock del contenido de username.txt
    mock_username = "test_user"
    
    # Mock de open para leer el archivo username.txt
    mock_open_read = mock_open(read_data=mock_username)
    
    # Mock del sistema de archivos para guardar el historial CSV
    mock_historial_csv = StringIO()
    
    with patch("builtins.open", mock_open_read):
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            crearHistorial(mock_data, None)
            
            # Validar que se leyó el archivo username.txt
            mock_open_read.assert_called_once_with("/app/temp/username.txt", "r")
            
            # Validar que se guardó el archivo historial.csv
            assert mock_to_csv.call_count == 1
            args, kwargs = mock_to_csv.call_args
            assert args[0] == '/app/temp/historial.csv'
            assert "index" in kwargs and kwargs["index"] is False
            assert "header" in kwargs and kwargs["header"] == ['usuario', 'rut', 'fecha', 'error', 'cambio']

def test_crear_historial_no_indices(mock_data):
    # Mock del contenido de username.txt
    mock_username = "test_user"
    
    # Mock de open para leer el archivo username.txt
    mock_open_read = mock_open(read_data=mock_username)
    
    # Mock del sistema de archivos para guardar el historial CSV
    mock_historial_csv = StringIO()
    
    with patch("builtins.open", mock_open_read):
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            crearHistorial(mock_data, [])
            
            # Validar que se procesó sin errores cuando indices es una lista vacía
            assert mock_to_csv.call_count == 1

def test_crear_historial_error(mock_data):
    # Simular un error al leer el archivo username.txt
    with patch("builtins.open", side_effect=FileNotFoundError):
        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            crearHistorial(mock_data, None)
            
            # Asegurarse de que no se intentó escribir el historial si hubo error
            assert mock_to_csv.call_count == 0
