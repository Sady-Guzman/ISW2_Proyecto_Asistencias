import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from depuracion import depurar_archivo, duplicados, faltaSalida, marcaOpuesto

class TestDepuracion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_path = os.path.join(os.path.dirname(__file__), '../Documentacion/marcajes_08-01-24.log')
        
        # Crear un archivo de reglas de prueba en el mismo directorio que test
        cls.reglas_path = os.path.join(os.path.dirname(__file__), 'horarios_mes_actual.csv')
        with open(cls.reglas_path, 'w', encoding='latin1') as f:
            f.write("Codigo,nombre,año,mes,entrada,salida,horaEn,minutoEn,horaSal,minutoSal\n")
            f.write("1,John,2024,01,08:00,17:00,8,0,17,0\n")
            f.write("2,Jane,2024,01,07:00,17:00,7,0,17,0\n")

        cls.marcaje = pd.read_csv(cls.file_path, header=None, sep=',', 
                                  names=["Codigo", "a", "entrada/salida", "rut", "b", "hora", "minuto", 
                                         "día", "mes", "año", "c", "d", "e", "f", "g", "h", "i", "j", "k"])

        if 'Hora' not in cls.marcaje.columns:
            cls.marcaje['Hora'] = cls.marcaje['hora'].astype(str).str.zfill(2) + ':' + cls.marcaje['minuto'].astype(str).str.zfill(2)
        if 'Error' not in cls.marcaje.columns:
            cls.marcaje['Error'] = 'Ok'

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.reglas_path)

    def test_duplicados(self):
        resultado = duplicados(self.marcaje)
        duplicados_encontrados = resultado[resultado['Error'] != 'Ok']
        self.assertGreater(len(duplicados_encontrados), 0, "Debería haber al menos un duplicado identificado")

    def test_faltaSalida(self):
        resultado = faltaSalida(self.marcaje, pd.read_csv(self.reglas_path, encoding='latin1'))
        salida_automatica = resultado[resultado['Error'].str.contains("Salida automatica corregida", na=False)]
        self.assertGreater(len(salida_automatica), 0, "Debería haber al menos una salida automática corregida")

    def test_marcaOpuesto(self):
        resultado = marcaOpuesto(self.marcaje, pd.read_csv(self.reglas_path, encoding='latin1'))
        marcas_opuestas = resultado[resultado['Error'].str.contains("invertida", na=False)]
        self.assertGreater(len(marcas_opuestas), 0, "Debería haber al menos una entrada/salida invertida corregida")

    def test_depurar_archivo(self):
        try:
            resultado = depurar_archivo(self.file_path, self.reglas_path)
            self.assertIsNotNone(resultado, "La función depurar_archivo debería devolver un valor, no None.")
        except Exception as e:
            self.fail(f"La función depurar_archivo falló con una excepción: {e}")

if __name__ == '__main__':
    unittest.main()

