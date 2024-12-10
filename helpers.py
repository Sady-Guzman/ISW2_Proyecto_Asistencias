import requests

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):

    return render_template("apology.html")

def user_login_required(f):
    """Decorador para requerir inicio de sesión de un usuario."""
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapped_function

def admin_login_required(f):
    """Decorador para requerir inicio de sesión de un administrador en una vista."""
    @wraps(f)
    def wrapped_admin_function(*args, **kwargs):
        if "user_id" not in session or not session.get("is_admin", False):
            return redirect("/adlogin")
        return f(*args, **kwargs)
    return wrapped_admin_function


def format_rut(rut):
    # Divide el RUT en la parte numérica y el dígito verificador.
    number_part, verifier_digit = rut.split('-')

    # Invierte la parte numérica para facilitar el formato.
    number_part = number_part[::-1]

    # Agrega puntos cada 3 dígitos.
    formatted_number = '.'.join([number_part[i:i+3] for i in range(0, len(number_part), 3)])

    # Invierte nuevamente para restaurar el orden original.
    formatted_number = formatted_number[::-1]

    # Retorna el RUT formateado.
    return f"{formatted_number}-{verifier_digit}"
