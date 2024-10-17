from flask import Flask, render_template, request, session, flash, redirect
from helpers import user_login_required
from werkzeug.security import generate_password_hash

from flask import Blueprint, render_template, request, session, redirect, flash

app = Blueprint('carga_archivo', __name__)

@app.route("/cargar", methods=["GET", "POST"])
@user_login_required
def carga_archivo():
    """Usuario sube archivo de marcajes al sistema"""
    
    if request.method == "GET":
        # Solo carga html 
        return render_template("carga.html")
    else:
        # Aun no se hace nada
        # return redirect("/")
        return render_template("apology.html")
