import os
import pytest
from app import app  # Asegúrate de que `app.py` y `test_app.py` estén en el mismo directorio

# Configuración para pruebas
app.config['TESTING'] = True
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'temp')
app.config['SECRET_KEY'] = 'clave_de_prueba'

@pytest.fixture
def client():
    """Fixture para crear un cliente de pruebas de Flask"""
    with app.test_client() as client:
        yield client

def test_index(client):
    """Prueba de la ruta principal '/'"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"index" in response.data  # Verifica que se cargue la página de índice correctamente

def test_subir_archivo_log_valido(client):
    """Prueba de subida de archivo con extensión válida (.log)"""
    with open('registro.log', 'w') as f:
        f.write('Contenido de prueba')  # Crea archivo de prueba temporal
    
    with open('registro.log', 'rb') as archivo:
        response = client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')
    
    os.remove('registro.log')  # Limpieza del archivo de prueba

    assert response.status_code == 302  # Redirección exitosa
    assert b'/visualizacion' in response.data  # Redirige a visualización

def test_sin_archivo(client):
    """Prueba sin archivo adjunto"""
    response = client.post('/cargar', data={}, content_type='multipart/form-data')
    assert response.status_code == 302
    assert b'No se detecta archivo' in response.data  # Mensaje de error correcto

def test_extension_invalida(client):
    """Prueba con archivo de extensión inválida"""
    with open('archivo.txt', 'w') as f:
        f.write('Contenido de prueba')
    
    with open('archivo.txt', 'rb') as archivo:
        response = client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')
    
    os.remove('archivo.txt')

    assert response.status_code == 302
    assert b'Tipo de archivo invalido' in response.data  # Mensaje de error correcto

def test_guardado_nombre_original(client):
    """Verifica el almacenamiento del nombre original del archivo subido"""
    with open('registro.log', 'w') as f:
        f.write('Contenido de prueba')

    with open('registro.log', 'rb') as archivo:
        client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')
    
    os.remove('registro.log')
    
    # Verificar contenido de NOMBRE_ORIGINAL_ARCHIVO.txt
    nombre_archivo = os.path.join(app.config['UPLOAD_FOLDER'], 'NOMBRE_ORIGINAL_ARCHIVO.txt')
    assert os.path.exists(nombre_archivo)  # El archivo de nombre original debe existir

    with open(nombre_archivo, 'r') as f:
        nombre_original = f.read().strip()
    
    assert nombre_original == 'registro.log'  # Nombre coincide

def test_archivo_guardado_como_csv(client):
    """Verifica que el archivo guardado tenga extensión .csv después de la depuración"""
    with open('registro.log', 'w') as f:
        f.write('Contenido de prueba')

    with open('registro.log', 'rb') as archivo:
        client.post('/cargar', data={'file': archivo}, content_type='multipart/form-data')
    
    os.remove('registro.log')
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'marcajes_original.csv')
    assert os.path.exists(file_path)  # El archivo .csv debería estar presente
