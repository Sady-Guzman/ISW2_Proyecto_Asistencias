import requests

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    # def escape(s):
    #     """
    #     Escape special characters.

    #     https://github.com/jacebrowning/memegen#special-characters
    #     """
    #     for old, new in [
    #         ("-", "--"),
    #         (" ", "-"),
    #         ("_", "__"),
    #         ("?", "~q"),
    #         ("%", "~p"),
    #         ("#", "~h"),
    #         ("/", "~s"),
    #         ('"', "''"),
    #     ]:
    #         s = s.replace(old, new)
    #     return s

    return render_template("apology.html")

# Descontinuado, Ahora existe version independiente para admin y usuario
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function



def user_login_required(f):
    """Decorator to require login for a user."""
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapped_function

def admin_login_required(f):
    """Decorator to require admin login for a view."""
    @wraps(f)
    def wrapped_admin_function(*args, **kwargs):
        if "user_id" not in session or not session.get("is_admin", False):
            return redirect("/adlogin")
        return f(*args, **kwargs)
    return wrapped_admin_function


def format_rut(rut):
    # Split the RUT into the number part and the verifier digit
    number_part, verifier_digit = rut.split('-')

    # Reverse the number part for easier formatting
    number_part = number_part[::-1]

    # Add periods every 3 digits
    formatted_number = '.'.join([number_part[i:i+3] for i in range(0, len(number_part), 3)])

    # Reverse it back to its original order
    formatted_number = formatted_number[::-1]

    # Return the formatted RUT
    return f"{formatted_number}-{verifier_digit}"