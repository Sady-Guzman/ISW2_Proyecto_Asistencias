from flask import Flask, render_template
from flask_session import Session
import os
from session_routes import session_routes
from manejo_cuentas import manejo_cuentas
from carga_archivo import carga_archivo
from visualizacion import visualizacion

'''

temp/marcajes_original.csv -> Nombre que se le asigna al archivo subido por usuario. Originalmente es .log
temp/datos_procesados.csv -> Nombre de archivo original despues de pasar por modulo de depuracion

'''

app = Flask(__name__)
app.config['DEBUG'] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# app.config['UPLOAD_FOLDER'] = 'temp'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'temp')  # or an absolute path
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Show index"""
    # Dejar vacio o poner informacin?
    return render_template("index.html")

# Import other apps (blueprints)
app.register_blueprint(session_routes)
app.register_blueprint(manejo_cuentas)
app.register_blueprint(carga_archivo)
app.register_blueprint(visualizacion)

if __name__ == "__main__":
    app.run()
