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


def test_PSA_001(client):
    """
    PSA-001: Prueba de subida de archivo con extensión válida (.log)
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


def test_PSA_002(client):
    """
    PSA-002: Prueba de envío sin archivo adjunto
    """
    response = client.post('/cargar', data={}, content_type='multipart/form-data')

    # Capturar mensajes flash desde la sesión.
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])
        assert ('error', 'No se detecta archivo') in flashed_messages
        
def test_PSA_003(client):
    """
    PSA-003: Subir un archivo con nombre vacío
    """
    # Simular envío de archivo sin nombre en los datos del formulario
    data = {
        'file': (b'Contenido de prueba', '')  # Archivo con contenido, pero sin nombre
    }

    response = client.post('/cargar', data=data, content_type='multipart/form-data')

    # Verificar redirección correcta
    assert response.status_code == 302
    assert response.location.endswith('/cargar')

    # Capturar mensajes flash desde la sesión
    with client.session_transaction() as session:
        flashed_messages = session.get('_flashes', [])
        assert ('error', 'No se detecta archivo') in flashed_messages



def test_PSA_004(client):
    """
    PSA-004: Prueba con archivo de extensión no permitida.
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



def test_PSA_005(client):
    """
    PSA 005: Verifica que el nombre original del archivo se guarde correctamente.
    """
    # Crear archivo de prueba
    with open('registro.log', 'w') as f:
        f.write('Contenido de prueba')

    # Simular la carga del archivo
    with open('registro.log', 'rb') as archivo:
        response = client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')

    # Limpieza del archivo local
    os.remove('registro.log')

    # Verificar redirección a la ruta esperada
    assert response.status_code == 302, "La carga no generó redirección como se esperaba."
    assert response.location.endswith('/visualizacion'), "La redirección no apunta a /visualizacion."

    # Verificar que el archivo con el nombre original exista
    nombre_archivo = "/app/temp/NOMBRE_ORIGINAL_ARCHIVO.txt"
    assert os.path.exists(nombre_archivo), "El archivo con el nombre original no se creó correctamente."

    # Verificar contenido del archivo
    with open(nombre_archivo, 'r') as f:
        contenido = f.read()
    assert contenido == 'registro.log', "El contenido del archivo de nombre original no es correcto."


def test_PSA_006(client):
    """
    PSA 006: Verifica que el archivo subido se guarde como .csv después de procesarse
    """
    with open('registro.log', 'w') as f:
        f.write('Contenido de prueba')

    with open('registro.log', 'rb') as archivo:
        client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')

    os.remove('registro.log')  # Limpieza del archivo local

    # Verificar que el archivo .csv exista
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'marcajes_original.csv')
    assert os.path.exists(file_path)
