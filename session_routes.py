from flask import Flask, render_template, request, session, redirect, flash
from helpers import user_login_required, admin_login_required
from werkzeug.security import check_password_hash, generate_password_hash

from flask import Blueprint, render_template, request, session, redirect, flash
from db import get_db  # Import from db.py

# app = Blueprint('session_routes', __name__)
session_routes = Blueprint('session_routes', __name__)

@session_routes.route("/login", methods=["GET", "POST"])
def login():
    """Log in del usurio"""
    
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            flash("Credenciales incorrectas. Debe ingresar nombre de usuario.", "error")
            return render_template("login.html")
        
        if request.form.get("username") == "admin":
            flash("Credenciales reservadas. Intente con otro usuario.", "error")
            return render_template("login.html")

        if not request.form.get("password"):
            flash("Credenciales incorrectas. Debe ingresar contraseña.", "error")
            return render_template("login.html")


        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()
        db.close()

        if len(rows) != 1 or not check_password_hash(rows[0][3], request.form.get("password")):
            flash("Credenciales incorrectas. Usuario/Contraseña.", "error")
            return render_template("login.html")

        session["user_id"] = rows[0][0]
        session["is_admin"] = False

        # Guardar nombre de usuario
        user = request.form.get("username")
        temp_path = "/app/temp/username.txt"

        # Guardar el nombre en el archivo
        with open(temp_path, "w") as file:
            file.write(user)
        
        return redirect("/")

    else:
        return render_template("login.html")

@session_routes.route("/adlogin", methods=["GET", "POST"])
def admin_login():
    """Log in de admin """
    
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            flash("Credenciales incorrectas. Debe ingresar un usuario.", "error")
            return render_template("adlogin.html")
        
        if request.form.get("username") != "admin":
            flash("Credenciales incorrectas. Debe usar cuenta de Administrador.", "error")
            return render_template("adlogin.html")

        if not request.form.get("password"):
            flash("Credenciales incorrectas. Debe ingresar contraseña.", "error")
            return render_template("adlogin.html")


        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()
        db.close()

        if len(rows) != 1 or not check_password_hash(rows[0][3], request.form.get("password")):
            flash("Credenciales incorrectas. Usuario o Contraseña incorrectos.", "error")
            return render_template("adlogin.html")
        
        session['is_admin'] = True 
        session["user_id"] = rows[0][0]
            
        return redirect("/")

    else:
        return render_template("adlogin.html")

@session_routes.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

