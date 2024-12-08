from flask import Flask, render_template
from flask_session import Session
import os
from session_routes import session_routes
from manejo_cuentas import manejo_cuentas
from carga_archivo import carga_archivo
from visualizacion import visualizacion
from subir_reglas import subir_reglas
'''

temp/marcajes_original.csv -> Nombre que se le asigna al archivo subido por usuario. Originalmente es .log
temp/datos_procesados.csv -> Nombre de archivo original despues de pasar por modulo de depuracion

./horario_mensual -> persistente, guarda horarios que sube admin cada mes.
'''

app = Flask(__name__)
app.jinja_env.globals.update(enumerate=enumerate)
app.config['DEBUG'] = True


# Configura la sesion para usar sistema de archivos en vez de cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# app.config['UPLOAD_FOLDER'] = 'temp'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'temp')
Session(app)

@app.after_request
def after_request(response):
    """Asegura que las respuestas no se guardan en cache"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    # Mostrar index como pagina de inicio
    return render_template("index.html")

# Importa los modulos (Blueprints)
app.register_blueprint(session_routes)
app.register_blueprint(manejo_cuentas)
app.register_blueprint(carga_archivo)
app.register_blueprint(visualizacion)
app.register_blueprint(subir_reglas)

if __name__ == "__main__":
    app.run()
