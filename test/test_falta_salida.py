# test_falta_salida.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from depuracion import faltaSalida

class TestFaltaSalida(unittest.TestCase):
    def test_faltaSalida(self):
        # Datos de prueba con la columna 'Hora' generada a partir de 'hora' y 'minuto'
        marcaje = pd.DataFrame([
            {"Codigo": "001", "entrada/salida": 1, "rut": "123", "hora": 0, "minuto": 0, "día": 2, "Error": "Ok"}
        ])
        
        # Crear la columna 'Hora' combinando 'hora' y 'minuto'
        marcaje['Hora'] = marcaje['hora'].astype(str).str.zfill(2) + ':' + marcaje['minuto'].astype(str).str.zfill(2)
        
        # Datos de prueba para las reglas de horario
        reglas = pd.DataFrame([
            {"Codigo": "001", "salida": "17:00", "horaSal": 17, "minutoSal": 0}
        ])
        
        # Llamada a la función faltaSalida y verificación de resultados
        result = faltaSalida(marcaje, reglas)
        
        # Verificar que la salida se ajustó correctamente
        salida_ajustada = result.iloc[0]
        self.assertEqual(salida_ajustada["hora"], 17, "La hora de salida debe ajustarse a 17")
        self.assertEqual(salida_ajustada["minuto"], 0, "El minuto de salida debe ajustarse a 0")

if __name__ == '__main__':
    unittest.main()
