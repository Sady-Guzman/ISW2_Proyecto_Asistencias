from flask import Flask, render_template, request, session, redirect, flash
from helpers import user_login_required, admin_login_required
from werkzeug.security import check_password_hash, generate_password_hash

from flask import Blueprint, render_template, request, session, redirect, flash
from db import get_db  # Import from db.py

# app = Blueprint('session_routes', __name__)
session_routes = Blueprint('session_routes', __name__)

@session_routes.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            # return apology("must provide username", 403)
            flash("Credenciales incorrectas. Debe ingresar nombre de usuario.", "error")
            return render_template("login.html")
        
        if request.form.get("username") == "admin":
            # return apology("Reserved username", 403)
            flash("Credenciales reservadas. Intente con otro usuario.", "error")
            return render_template("login.html")

        if not request.form.get("password"):
            # return apology("must provide password", 403)
            flash("Credenciales incorrectas. Debe ingresar contraseña.", "error")
            return render_template("login.html")


        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()
        db.close()

        if len(rows) != 1 or not check_password_hash(rows[0][3], request.form.get("password")):
            # return apology("invalid username/password", 403)
            flash("Credenciales incorrectas. Usuario/Contraseña.", "error")
            return render_template("login.html")

        session["user_id"] = rows[0][0]
        session["is_admin"] = False
        
        return redirect("/")

    else:
        return render_template("login.html")

@session_routes.route("/adlogin", methods=["GET", "POST"])
def admin_login():
    """Log admin in"""
    
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            # return apology("must provide admin username", 403)
            flash("Credenciales incorrectas. Debe ingresar un usuario.", "error")
            return render_template("adlogin.html")
        
        if request.form.get("username") != "admin":
            # return apology("Invalid ADMIN user", 403)
            flash("Credenciales incorrectas. Debe usar cuenta de Administrador.", "error")
            return render_template("adlogin.html")

        if not request.form.get("password"):
            # return apology("must provide admin password", 403)
            flash("Credenciales incorrectas. Debe ingresar contraseña.", "error")
            return render_template("adlogin.html")


        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()
        db.close()

        if len(rows) != 1 or not check_password_hash(rows[0][3], request.form.get("password")):
            # return apology("invalid username and/or password", 403)
            flash("Credenciales incorrectas. Usuario o Contraseña incorrectos.", "error")
            return render_template("adlogin.html")
        
        session['is_admin'] = True  # or False for normal users
        session["user_id"] = rows[0][0]
            
        return redirect("/")

    else:
        return render_template("adlogin.html")

@session_routes.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

