import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from depuracion import depurar_archivo, duplicados, faltaSalida, marcaOpuesto, registraSalida

# Prueba 1: Duplicados
def test_duplicados():
    # Crear un DataFrame simulado con duplicados
    data = {
        "rut": ["123", "123", "123"],
        "día": [1, 1, 1],
        "Hora": ["08:00", "08:30", "08:45"],
        "entrada/salida": ["01", "01", "03"],
    }
    df = pd.DataFrame(data)

    # Ejecutar la función
    resultado = duplicados(df)

    # Comprobar si el DataFrame procesado contiene las filas corregidas
    assert len(resultado) == 4  # Se debería agregar una salida ficticia
    assert resultado.iloc[-1]["entrada/salida"] == "03"  # La salida generada

# Prueba 2: Registra salida
def test_registra_salida():
    # Crear un DataFrame simulado
    data = {
        "rut": ["123", "123"],
        "día": [1, 1],
        "Hora": ["08:00", "18:00"],
        "entrada/salida": ["01", "03"],
        "cierre": ["No tiene cierre", "No tiene cierre"],
    }
    df = pd.DataFrame(data)

    # Ejecutar la función
    registraSalida(df, 0)

    # Comprobar que los cierres sean correctos
    assert df.at[0, "cierre"] == "Tiene cierre"
    assert df.at[1, "cierre"] == "Tiene cierre"

# Prueba 3: Falta salida
def test_falta_salida():
    # Crear DataFrame simulado para marcaje
    marcaje = pd.DataFrame({
        "rut": ["123"],
        "día": [1],
        "hora": [8],
        "minuto": [0],
        "entrada/salida": ["01"],
        "cierre": ["No tiene cierre"],
        "Codigo": [1],
        "Hora": ["08:00"],
    })

    # Crear DataFrame simulado para reglas
    reglas = pd.DataFrame({
        "Codigo": [1],
        "horaSal": [18],
        "minutoSal": [0],
        "salida": ["18:00"],
    })

    # Ejecutar la función
    resultado = faltaSalida(marcaje, reglas)

    # Comprobar que se agregó una salida
    assert len(resultado) == 2
    assert resultado.iloc[-1]["entrada/salida"] == "03"  # La salida generada
    assert resultado.iloc[-1]["Hora"] == "18:00"  # La hora generada

# Prueba 4: Marca opuesto
def test_marca_opuesto():
    # Crear DataFrame simulado
    marcaje = pd.DataFrame({
        "rut": ["123"],
        "hora": [18],
        "minuto": [5],
        "entrada/salida": ["01"],
        "Error": ["Ok"],
        "cierre": ["No tiene cierre"],
        "Codigo": [1],
    })

    reglas = pd.DataFrame({
        "Codigo": [1],
        "horaSal": [18],
        "minutoSal": [0],
    })

    # Ejecutar la función
    resultado = marcaOpuesto(marcaje, reglas)

    # Comprobar que se corrigió la marca
    assert resultado.iloc[0]["entrada/salida"] == "03"  # Entrada corregida a salida
    assert "Entrada invertida a salida" in resultado.iloc[0]["Error"]

# Prueba 5: Depuración completa
def test_depurar_archivo(mocker):
    # Mockear archivos de entrada
    mocker.patch("pandas.read_csv", side_effect=[
        pd.DataFrame({
            "Codigo": [1],
            "a": [""],
            "entrada/salida": ["01"],
            "rut": ["123"],
            "b": [""],
            "hora": [8],
            "minuto": [0],
            "mes": [1],
            "día": [1],
            "año": [2024],
            "c": [""],
            "d": [""],
            "e": [""],
            "f": [""],
            "g": [""],
            "h": [""],
            "i": [""],
            "j": [""],
            "k": [""],
        }),
        pd.DataFrame({
            "Codigo": [1],
            "horaSal": [18],
            "minutoSal": [0],
            "salida": ["18:00"],
        }),
    ])

    # Ejecutar la función principal
    resultado = depurar_archivo("/path/to/mock.log")

    # Comprobar que el resultado no sea `None`
    assert resultado is not None