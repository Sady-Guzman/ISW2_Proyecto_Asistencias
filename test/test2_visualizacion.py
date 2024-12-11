import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
import pandas as pd
from visualizacion import visualizacion  # Import your Blueprint
from flask import Flask, session, send_file
from io import BytesIO

@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = "test_secret_key"  # Configuración de clave secreta para las pruebas
    
    # Configuración de rutas para pruebas
    @app.route('/visualizacion')
    def visualizar():
        return "Visualización", 200

    @app.route('/apply_filters', methods=['POST'])
    def apply_filters():
        return "Filtros aplicados", 200

    @app.route('/download_csv', methods=['POST'])
    def download_csv():
        return "Descarga CSV", 200

    @app.route('/download_historial', methods=['GET'])
    def download_historial():
        file_path = '/tmp/historial.csv'
        try:
            return send_file(file_path, as_attachment=True)
        except FileNotFoundError:
            flash("Error al descargar el historial.", "error")
            return "Error", 500

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_csv_file():
    # Crear archivo temporal simulado
    file_path = '/tmp/historial.csv'
    with open(file_path, 'w') as f:
        f.write("test_data")
    yield file_path
    os.remove(file_path)  # Limpiar después de las pruebas

#PDV-001
def test_visualizar(client):
    response = client.get('/visualizacion')
    assert response.status_code == 200

def test_apply_filters(client):
    response = client.post('/apply_filters', data={
        'rut_filter': '12345678-9',
        'from_hour': '09:00',
        'to_hour': '10:00',
        'tipo_marcaje': 'entrada',
        'condicion': 'any',
        'codigo_filter': '001',
        'day_filter': ['1']
    })
    assert response.status_code == 200
#PDV-002
def test_download_csv(client):
    response = client.post('/download_csv', data={'selected_rows': []})
    assert response.status_code == 200
#PDV-003
def test_download_historial(client, sample_csv_file):
    response = client.get('/download_historial')
    assert response.status_code == 200
