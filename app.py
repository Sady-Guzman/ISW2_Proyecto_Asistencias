from flask import Flask, render_template
from flask_session import Session
from session_routes import app as session_routes
from manejo_cuentas import app as manejo_cuentas
from carga_archivo import app as carga_archivo

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
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

if __name__ == "__main__":
    app.run()
