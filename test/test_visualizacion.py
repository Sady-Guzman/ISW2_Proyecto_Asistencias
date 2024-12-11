import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from flask import Flask
from visualizacion import visualizacion
from app import app

@pytest.fixture
def client():
    """Fixture para inicializar la aplicación y configurar un cliente de pruebas."""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = '/app/temp'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['user_id'] = 1  # Simula usuario autenticado
        yield client

    # Limpieza del directorio temporal
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))


@pytest.fixture
def setup_csv():
    """Fixture para crear un archivo CSV de prueba."""
    file_path = '/app/temp/datos_procesados.csv'
    df = pd.DataFrame({
        'rut': ['12345', '67890'],
        'hora': [8, 9],
        'marcaje': ['entrada', 'salida']
    })
    df.to_csv(file_path, index=False)
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)

#PVD-004
def test_visualizar_archivo_no_disponible(client):
    response = client.get('/visualizacion')

    assert response.status_code == 302
    assert response.location.endswith('/cargar')

#PVD-005
def test_acceso_no_autenticado_visualizacion():
    with app.test_client() as client:
        response = client.get('/visualizacion')
        assert response.status_code == 302
        assert response.location.endswith('/login')
        

