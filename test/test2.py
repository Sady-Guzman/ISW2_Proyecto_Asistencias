import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from depuracion import depurar_archivo, duplicados, faltaSalida, marcaOpuesto

class TestDepuracion(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Cargar archivo de marcaje y reglas de horario simuladas
        cls.file_path = "C:/Users/Daniel/Documents/GitHub/ISW2_Proyecto_Asistencias/Documentacion/marcajes_08-01-24.log"

        # Reglas de horario de ejemplo
        reglas_data = """1,John,2024,01,08:00,17:00,8,0,17,0
                         2,Jane,2024,01,07:00,17:00,7,0,17,0"""
        
        cls.reglas = pd.read_csv(pd.io.common.StringIO(reglas_data), sep=",",
                                 names=["Codigo", "nombre", "año", "mes", "entrada", "salida", 
                                        "horaEn", "minutoEn", "horaSal", "minutoSal"])

        # Leer el archivo log proporcionado como DataFrame de prueba
        cls.marcaje = pd.read_csv(cls.file_path, header=None, sep=',', 
                                  names=["Codigo", "a", "entrada/salida", "rut", "b", "hora", "minuto", 
                                         "día", "mes", "año", "c", "d", "e", "f", "g", "h", "i", "j", "k"])

    def test_duplicados(self):
        # Prueba el manejo de duplicados
        resultado = duplicados(self.marcaje)
        duplicados_encontrados = resultado[resultado['Error'] != 'Ok']
        self.assertGreater(len(duplicados_encontrados), 0, "Debería haber al menos un duplicado identificado")

    def test_faltaSalida(self):
        # Prueba el manejo de falta de salida
        resultado = faltaSalida(self.marcaje, self.reglas)
        salida_automatica = resultado[resultado['Error'].str.contains("Salida automatica corregida", na=False)]
        self.assertGreater(len(salida_automatica), 0, "Debería haber al menos una salida automática corregida")

    def test_marcaOpuesto(self):
        # Prueba el manejo de marcas opuestas
        resultado = marcaOpuesto(self.marcaje, self.reglas)
        marcas_opuestas = resultado[resultado['Error'].str.contains("invertida", na=False)]
        self.assertGreater(len(marcas_opuestas), 0, "Debería haber al menos una entrada/salida invertida corregida")

    def test_depurar_archivo(self):
        # Prueba principal del método depurar_archivo
        try:
            resultado = depurar_archivo(self.file_path)
            self.assertIsNotNone(resultado, "La función depurar_archivo debería devolver un valor, no None.")
        except Exception as e:
            self.fail(f"La función depurar_archivo falló con una excepción: {e}")

if __name__ == '__main__':
    unittest.main()
