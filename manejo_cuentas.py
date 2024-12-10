from flask import Flask, render_template, request, session, flash, redirect
from helpers import admin_login_required, format_rut
from werkzeug.security import generate_password_hash

from flask import Blueprint, render_template, request, session, redirect, flash
from db import get_db  # Import from db.py

# app = Blueprint('manejo_cuentas', __name__)
manejo_cuentas = Blueprint('manejo_cuentas', __name__)

@manejo_cuentas.route("/register", methods=["GET", "POST"])
@admin_login_required
def register():
    """Registrar nuevo usuario"""
    
    if request.method == "GET":
        # Cuando es GET simplemente muestra la página de registro
        return render_template("register.html")
    else:
        # Cuando es POST, registra nuevo usuario

        rut_input = request.form.get("rut")

        # Asegura que el RUT fue ingresado
        if not request.form.get("rut"):
            flash("Debe ingresar RUT.", "error")
            return render_template("register.html") 
        
        if len(rut_input) > 10 or len(rut_input) < 9 or '.' in rut_input or '-' not in rut_input:
            flash("RUT no puede tener puntos y debe tener guion.", "error")
            return render_template("register.html") 
        
        # Asegura que el nombre de usuario fue ingresado
        if not request.form.get("username"):
            flash("Debe ingresar un nombre de usuario.", "error")
            return render_template("register.html") 

        # Asegura que la contraseña fue ingresada
        elif not request.form.get("password"):
            flash("Debe ingresar una contraseña.", "error")
            return render_template("register.html") 

        # Asegura que la contraseña fue ingresada nuevamente
        elif not request.form.get("confirmation"):
            flash("Debe ingresar confirmación de contraseña.", "error")
            return render_template("register.html") 

        # Asegura que la contraseña y la confirmación de la contraseña coincidan
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("ERROR: Contraseña y confirmación no son iguales.", "error")
            return render_template("register.html") 

        # Logica SQL 
        db = get_db()
        cursor = db.cursor()

        # Query database para username
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()

        # Asegurar que username no exista
        if len(rows) != 0:
            flash("ERROR: Nombre de usuario ya esta en uso!", "error")
            return render_template("register.html") 
        else:
            # Si todo esta OK, registra nuevo usuario, rut, and la contraseña con hash en la DB
            cursor.execute("INSERT INTO users (rut, username, hash) VALUES (%s, %s, %s)", 
                           (request.form.get("rut"), request.form.get("username"), generate_password_hash(request.form.get("password"))))
            db.commit()  # Commit la transaccion para guardar cambios

        cursor.close()  # Cerrar el cursor
        db.close()  # Cerrar la conexión con la DB

        # Redireccionar al usuario al login form
        return redirect("/")

@manejo_cuentas.route("/change_password", methods=["GET", "POST"])
@admin_login_required
def change_password():
    """Cambiar contraseña del usuario seleccionado"""
    
    if request.method == "GET":
        # En caso de GET, simplemente muestra la página para cambiar la contraseña
        return render_template("edit_account.html")
    else:
        # En caso de POST, cambia la contraseña

        # Asegurar que se ingresó un nombre de usuario
        if not request.form.get("username"):
            flash("Debe ingresar nombre de usuario.", "error")
            return render_template("login.html")

        # Asegurar que se ingresó una nueva contraseña
        elif not request.form.get("password"):
            flash("Debe ingresar una contraseña.", "error")
            return render_template("login.html")

        # Asegurar que se confirmó la nueva contraseña
        elif not request.form.get("confirmation"):
            flash("Debe confirmar contraseña.", "error")
            return render_template("login.html")

        # Asegurar que la contraseña y la confirmación coincidan
        elif request.form.get("password") != request.form.get("confirmation"):
            flash("ERROR: Contraseña y confirmación no son iguales.", "error")
            return render_template("login.html")

        # Lógica SQL
        db = get_db() 
        cursor = db.cursor()

        # Verifica si existe el nombre de usuario especificado
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        user = cursor.fetchone()

        if user is None:
            flash("ERROR: No se encuentra ninguna cuenta con ese usuario.", "error")
            return render_template("edit_account.html")
            
        # No hay ningún problema
        # Actualiza la contraseña en la base de datos
        cursor.execute("UPDATE users SET hash = %s WHERE username = %s", 
                       (generate_password_hash(request.form.get("password")), request.form.get("username")))
        db.commit()  # Confirma la transacción para guardar los cambios

        cursor.close()  # Cierra el cursor
        db.close()  # Cierra la conexión a la base de datos

        # Redirige al usuario después de cambiar la contraseña
        return redirect("/")


@manejo_cuentas.route("/view_accounts")
@admin_login_required
def view_accounts():
    """Ver todas las cuentas de usuario"""
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, rut, username FROM users")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    
    # Pone puntos en rut, Mantiene guion
    usuarios_formateados = [(user[0], format_rut(user[1]), user[2]) for user in users]
    
    return render_template("view_accounts.html", users=usuarios_formateados)


@manejo_cuentas.route("/delete_account", methods=["POST"])
@admin_login_required
def delete_account():
    """Eliminar cuenta de usuario"""
    from flask import request, flash, redirect
    
    user_id = request.form.get("user_id")
    
    if not user_id:
        flash("ID de usuario no proporcionado.", "warning")
        return redirect("/view_accounts")
    
    try:
        db = get_db()
        cursor = db.cursor()
        # Eliminar el usuario con el proporcionado ID
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.commit()
        cursor.close()
        db.close()
        
        flash("Usuario eliminado exitosamente.", "success")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")
        flash("Hubo un error al intentar eliminar el usuario.", "danger")
    
    return redirect("/view_accounts")
