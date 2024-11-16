import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import app

@pytest.fixture
def client():
    """
    Configuración del cliente de pruebas con:
    - Creación de directorio para archivos subidos
    - Simulación de sesión autenticada
    """
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'temp')  # Directorio de subida

    # Crear el directorio si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Crear cliente de pruebas
    with app.test_client() as client:
        # Simular sesión autenticada
        with client.session_transaction() as session:
            session['user_id'] = 1  # Simula un usuario autenticado
        yield client

    # Limpieza del directorio después de las pruebas
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isfile(file_path):
            os.unlink(file_path)


def test_subir_archivo_log_valido(client):
    """
    Prueba de subida de archivo con extensión válida (.log)
    """
    # Crear un archivo de prueba
    with open('registro.log', 'w') as f:
        f.write('Contenido de prueba')

    with open('registro.log', 'rb') as archivo:
        response = client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')

    os.remove('registro.log')  # Limpieza del archivo local

    # Verificar redirección exitosa
    assert response.status_code == 302
    assert b'/visualizacion' in response.data


def test_sin_archivo(client):
    """
    Prueba de envío sin archivo adjunto
    """
    response = client.post('/cargar', data={}, content_type='multipart/form-data')

    # Capturar mensajes flash desde la sesión.
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])
        assert ('error', 'No se detecta archivo') in flashed_messages


def test_extension_invalida(client):
    """
    Prueba con archivo de extensión no permitida.
    """
    # Crear un archivo con extensión no válida.
    with open('archivo.txt', 'w') as f:
        f.write('Contenido de prueba')

    with open('archivo.txt', 'rb') as archivo:
        response = client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')

    os.remove('archivo.txt')  # Limpieza del archivo local.

    # Verificar redirección correcta.
    assert response.status_code == 302
    assert response.location.endswith('/cargar')

    # Capturar mensajes flash desde la sesión.
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])
        assert ('error', 'Tipo de archivo invalido, Intente nuevamente con un archivo tipo .log') in flashed_messages



def test_guardado_nombre_original(client):
    """
    Verifica que el nombre original del archivo se guarde correctamente
    """
    with open('registro.log', 'w') as f:
        f.write('Contenido de prueba')

    with open('registro.log', 'rb') as archivo:
        client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')

    os.remove('registro.log')  # Limpieza del archivo local

    # Verificar que el archivo de nombre original exista
    nombre_archivo = os.path.join(app.config['UPLOAD_FOLDER'], 'NOMBRE_ORIGINAL_ARCHIVO.txt')
    assert os.path.exists(nombre_archivo)

    # Verificar contenido del archivo
    with open(nombre_archivo, 'r') as f:
        contenido = f.read()
    assert contenido == 'registro.log'


def test_archivo_guardado_como_csv(client):
    """
    Verifica que el archivo subido se guarde como .csv después de procesarse
    """
    with open('registro.log', 'w') as f:
        f.write('Contenido de prueba')

    with open('registro.log', 'rb') as archivo:
        client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')

    os.remove('registro.log')  # Limpieza del archivo local

    # Verificar que el archivo .csv exista
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'marcajes_original.csv')
    assert os.path.exists(file_path)
