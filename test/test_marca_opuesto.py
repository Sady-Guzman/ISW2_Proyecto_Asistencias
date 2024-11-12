# test_marca_opuesto.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import pandas as pd
from depuracion import marcaOpuesto

class TestMarcaOpuesto(unittest.TestCase):
    def test_marcaOpuesto(self):
        # Prueba para la corrección de acción opuesta
        marcaje = pd.DataFrame([
            {"Codigo": "001", "entrada/salida": 3, "rut": "123", "hora": 8, "minuto": 10, "Error": "Ok"}
        ])
        reglas = pd.DataFrame([
            {"Codigo": "001", "horaEn": 8, "minutoEn": 0, "horaSal": 17, "minutoSal": 0}
        ])
        result = marcaOpuesto(marcaje, reglas)
        entrada_ajustada = result.iloc[0]
        self.assertEqual(entrada_ajustada["entrada/salida"], 1, "La marca de salida incorrecta debe corregirse a entrada")

if __name__ == '__main__':
    unittest.main()
