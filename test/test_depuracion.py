import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import pytest
from depuracion import depurar_archivo # Importar funciones del módulo


@pytest.fixture
def log_file_reloj(tmp_path):
    """
    Copia el archivo reloj_dias_05-06.log al directorio temporal para su uso en las pruebas.
    """
    source_path = "/app/Documentacion/reloj_dias_05-06.log"  # Ruta del archivo original
    target_path = tmp_path / "reloj_dias_05-06.log"
    with open(source_path, "r") as source, open(target_path, "w") as target:
        target.write(source.read())
    return target_path

@pytest.fixture
def reglas_file(tmp_path):
    """
    Crea un archivo CSV de reglas para la prueba.
    """
    reglas_data = """Codigo,nombre,año,mes,entrada,salida,horaEn,minutoEn,horaSal,minutoSal
1,Regla1,2024,12,08:30,17:30,8,30,17,30
2,Regla2,2024,12,09:15,18:00,9,15,18,0"""
    reglas_path = tmp_path / "horarios_creados.csv"
    reglas_path.write_text(reglas_data)
    return reglas_path

def test_depurar_archivo_with_reloj_dias_log(log_file_reloj, reglas_file, monkeypatch, tmp_path):
    """
    Prueba la función depurar_archivo utilizando el archivo reloj_dias_05-06.log y un archivo de reglas.
    """
    # Guardar la referencia original de pd.read_csv
    original_read_csv = pd.read_csv

    # Mockear la ruta del archivo de reglas
    def mock_read_csv(path, *args, **kwargs):
        if "horarios_creados.csv" in str(path):
            return original_read_csv(reglas_file, *args, **kwargs)
        return original_read_csv(path, *args, **kwargs)

    monkeypatch.setattr("pd.read_csv", mock_read_csv)

    # Ejecutar la función depurar_archivo
    depurar_archivo(log_file_reloj)

    # Verificar que se haya creado el archivo procesado
    processed_file = "/app/temp/datos_procesados.csv"
    assert os.path.exists(processed_file), "El archivo procesado no fue creado"

    # Leer el archivo procesado y verificar su contenido
    processed_data = pd.read_csv(processed_file)
    assert not processed_data.empty, "El archivo procesado está vacío"

    # Validar algunas columnas clave
    assert "Hora" in processed_data.columns, "La columna 'Hora' no está presente"
    assert "Error" in processed_data.columns, "La columna 'Error' no está presente"

    # Imprimir para inspección manual (opcional)
    print(processed_data)