from flask import Flask, render_template, request, session, flash, redirect
from helpers import admin_login_required, format_rut
from werkzeug.security import generate_password_hash

from flask import Blueprint, render_template, request, session, redirect, flash
from db import get_db  # Import from db.py

app = Blueprint('manejo_cuentas', __name__)

@app.route("/register", methods=["GET", "POST"])
@admin_login_required
def register():
    """Register new user"""
    
    if request.method == "GET":
        # In case of GET simply shows register page
        return render_template("register.html")
    else:
        # In case of POST method, Register new user

        rut_input = request.form.get("rut")

        # Ensure RUT was submitted
        if not request.form.get("rut"):
            flash("Debe ingresar RUT.", "error")
            return render_template("register.html") 
        
        if len(rut_input) > 10 or len(rut_input) < 9 or '.' in rut_input or '-' not in rut_input:
            flash("RUT no puede tener puntos y debe tener guion.", "error")
            return render_template("register.html") 
        
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Debe ingresar un nombre de usuario.", "error")
            return render_template("register.html") 

        # Ensure password was submitted
        elif not request.form.get("password"):
            # return apology("must provide password", 400)
            flash("Debe ingresar una contraseña.", "error")
            return render_template("register.html") 

        # Ensure confirmed password was submitted
        elif not request.form.get("confirmation"):
            # return apology("must confirm password", 400)
            flash("Debe ingresar confirmación de contraseña.", "error")
            return render_template("register.html") 

        # Ensure password and confirmed password match
        elif request.form.get("password") != request.form.get("confirmation"):
            # return apology("password fields don't match", 400)
            flash("ERROR: Contraseña y confirmación no son iguales.", "error")
            return render_template("register.html") 

        # SQL Logic
        db = get_db()
        cursor = db.cursor()

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()

        # Ensure username is not already taken
        if len(rows) != 0:
            flash("ERROR: Nombre de usuario ya esta en uso!", "error")
            return render_template("register.html") 
        else:
            # In case everything is OK, register the new user, rut, and the hashed password into the DB
            cursor.execute("INSERT INTO users (rut, username, hash) VALUES (%s, %s, %s)", 
                           (request.form.get("rut"), request.form.get("username"), generate_password_hash(request.form.get("password"))))
            db.commit()  # Commit the transaction to save changes

        cursor.close()  # Close the cursor
        db.close()  # Close the database connection

        # Redirect user to login form
        return redirect("/")

@app.route("/change_password", methods=["GET", "POST"])
@admin_login_required
def change_password():
    """Change password of a specified user"""
    
    if request.method == "GET":
        # In case of GET, simply show the change password page
        return render_template("edit_account.html")
    else:
        # In case of POST method, change the password

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Debe ingresar nombre de usuario.", "error")
            return render_template("login.html")

        # Ensure new password was submitted
        elif not request.form.get("password"):
            flash("Debe ingresar una contraseña.", "error")
            return render_template("login.html")

        # Ensure new password was confirmed
        elif not request.form.get("confirmation"):
            flash("Debe confirmar contraseña.", "error")
            return render_template("login.html")

        # Ensure password and confirmed password match
        elif request.form.get("password") != request.form.get("confirmation"):
            # return apology("new password fields don't match", 400)
            flash("ERROR: Contraseña y confirmación no son iguales.", "error")
            return render_template("login.html")

        # SQL Logic
        db = get_db()  # Assuming you have a function to get the database connection
        cursor = db.cursor()

        # Check if the specified username exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        user = cursor.fetchone()

        if user is None:
            flash("ERROR: No se encuentra ninguna cuenta con ese usuario.", "error")
            return render_template("edit_account.html")
            
        # No hay ningun problema
        # Update the password in the database
        cursor.execute("UPDATE users SET hash = %s WHERE username = %s", 
                       (generate_password_hash(request.form.get("password")), request.form.get("username")))
        db.commit()  # Commit the transaction to save changes

        cursor.close()  # Close the cursor
        db.close()  # Close the database connection

        # Redirect user after changing the password
        return redirect("/")

@app.route("/view_accounts")
@admin_login_required
def view_accounts():
    """View all user accounts"""
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, rut, username FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    
    # Pone puntos en rut, Mantiene guion
    usuarios_formateados = [(user[0], format_rut(user[1]), user[2]) for user in users]
    
    return render_template("view_accounts.html", users=usuarios_formateados)

