import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from depuracion import depurar_archivo, duplicados, faltaSalida, marcaOpuesto

@pytest.fixture
def sample_data():
    """Fixture para crear datos de prueba simulados."""
    data = pd.DataFrame({
        "Codigo": ["1", "1"],
        "a": ["", ""],
        "entrada/salida": ["01", "03"],
        "rut": ["12345", "12345"],
        "b": ["", ""],
        "hora": [8, 17],
        "minuto": [0, 0],
        "mes": [1, 1],
        "día": [1, 1],
        "año": [2024, 2024],
        "c": ["", ""],
        "d": ["", ""],
        "e": ["", ""],
        "f": ["", ""],
        "g": ["", ""],
        "h": ["", ""],
        "i": ["", ""],
        "j": ["", ""],
        "k": ["", ""]
    })
    
    # Crear la columna 'Hora' concatenando 'hora' y 'minuto'
    data['Hora'] = data['hora'].astype(str).str.zfill(2) + ':' + data['minuto'].astype(str).str.zfill(2)
    
    return data

@pytest.fixture
def sample_rules():
    """Fixture para crear reglas de horarios simulados."""
    rules = pd.DataFrame({
        "Codigo": [1],
        "nombre": ["Test"],
        "año": [2024],
        "mes": [1],
        "entrada": ["08:00"],
        "salida": ["17:00"],
        "horaEn": [8],
        "minutoEn": [0],
        "horaSal": [17],
        "minutoSal": [0]
    })
    return rules

#PDD-001
def test_duplicados(sample_data):
    """Test para verificar duplicados."""
    result = duplicados(sample_data)
    assert not result.empty, "El resultado no debe estar vacío."
    assert "Error" in result.columns, "Debe incluir la columna 'Error'."
#PDD-002
def test_falta_salida(sample_data, sample_rules):
    """Test para verificar corrección de salidas faltantes."""
    sample_data["cierre"] = ["No tiene cierre", "Tiene cierre"]
    result = faltaSalida(sample_data, sample_rules)
    assert not result.empty, "El resultado no debe estar vacío."
    assert result["entrada/salida"].str.contains("03").any(), "Debe incluir salidas creadas automáticamente."
#PDD-003
def test_marca_opuesto(sample_data, sample_rules):
    """Test para verificar corrección de marcas invertidas."""
    result = marcaOpuesto(sample_data, sample_rules)
    assert not result.empty, "El resultado no debe estar vacío."
    assert result["entrada/salida"].isin(["01", "03"]).all(), "Debe corregir marcas invertidas."
#PDD-004
def test_depurar_archivo(tmp_path):
    """Test de integración para la función depurar_archivo."""
    # Crear archivo de prueba
    input_file = tmp_path / "test_file.log"
    data = "1,,01,12345,,,8,0,1,1,2024,,,,,,,,,\n" \
           "1,,03,12345,,,17,0,1,1,2024,,,,,,,,,\n"
    input_file.write_text(data)

    # Llamar la función
    result = depurar_archivo(str(input_file))

    assert result is None or isinstance(result, pd.DataFrame), "Debe devolver None o un DataFrame."

