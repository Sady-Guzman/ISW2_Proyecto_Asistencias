import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from io import StringIO
from depuracion import depurar_archivo, duplicados, faltaSalida, marcaOpuesto

class TestDepuracion(unittest.TestCase):

    def setUp(self):
        # DataFrame simulado para pruebas
        self.marcaje_data = StringIO("""
        1,0,1,12345678,0,9,0,1,1,2024,0,0,0,0,0,0,0,0
        1,0,1,12345678,0,9,0,1,1,2024,0,0,0,0,0,0,0,0
        1,0,3,12345678,0,9,0,1,1,2024,0,0,0,0,0,0,0,0
        1,0,1,87654321,0,9,0,1,1,2024,0,0,0,0,0,0,0,0
        1,0,3,87654321,0,9,0,1,1,2024,0,0,0,0,0,0,0,0
        """)
        self.reglas_data = StringIO("""
        Codigo,horaEn,minutoEn,horaSal,minutoSal,salida
        1,9,0,17,0,1
        """)

        # Cargar los DataFrames
        self.marcaje_df = pd.read_csv(self.marcaje_data, header=None, names=["Codigo", "a", "entrada/salida", "rut", "b", "hora", "minuto", "día", "mes", "año", "c", "d", "e", "f", "g", "h", "i", "j", "k"])
        self.reglas_df = pd.read_csv(self.reglas_data)

    def test_duplicados(self):
        result = duplicados(self.marcaje_df)
        self.assertIn('Error', result.columns)
        self.assertEqual(result['Error'].iloc[0], 'Entrada duplicada')
        self.assertEqual(result['Error'].iloc[2], 'Salida duplicada')

    def test_faltaSalida(self):
        marcaje_test = self.marcaje_df.copy()
        marcaje_test.at[0, 'Hora'] = '00:00'  # Simular una salida automática
        result = faltaSalida(marcaje_test, self.reglas_df)
        self.assertIn('Error', result.columns)
        self.assertIn('Salida automatica detectada', result['Error'].iloc[0])

    def test_marcaOpuesto(self):
        marcaje_test = self.marcaje_df.copy()
        marcaje_test.at[0, 'hora'] = 9
        marcaje_test.at[0, 'minuto'] = 0
        marcaje_test.at[0, 'entrada/salida'] = 3  # Simular una salida
        result = marcaOpuesto(marcaje_test, self.reglas_df)
        self.assertEqual(result.at[0, 'entrada/salida'], 1)  # Debe corregir a entrada

    def test_depurar_archivo(self):
        # Para este test, deberíamos simular la creación de un archivo procesado
        processed_file_path = depurar_archivo("marcajes_08-01-24.log")
        self.assertIsNotNone(processed_file_path)
        self.assertTrue(processed_file_path.endswith("_processed.csv"))

if __name__ == '__main__':
    unittest.main()