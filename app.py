import os
import psycopg2
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Custom filter
# app.jinja_env.filters["usd"] = lambda value: f"${value:,.2f}"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")  # Use environment variable for PostgreSQL connection

def get_db():
    """Connect to the PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code

def login_required(f):
    """Decorator to require login for a view."""
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
# @login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            # return apology("must provide username", 403)
            flash("Invalid credentials. Please provide a username.", "error")
            return render_template("login.html")
        
        if request.form.get("username") == "admin":
            # return apology("Reserved username", 403)
            flash("Invalid credentials. Reserved username, try with other username.", "error")
            return render_template("login.html")

        if not request.form.get("password"):
            # return apology("must provide password", 403)
            flash("Invalid credentials. Must provide password.", "error")
            return render_template("login.html")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()
        db.close()

        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            # return apology("invalid username/password", 403)
            flash("Invalid credentials. Invalid username or password.", "error")
            return render_template("login.html")

        session["user_id"] = rows[0][0]
        
        # Hardcoded check for admin user
        if rows[0][0] == 1:  # Replace 1 with the actual hardcoded admin user ID
            session["is_admin"] = True
        else:
            session["is_admin"] = False
            
        
        return redirect("/")

    else:
        return render_template("login.html")
    
@app.route("/adlogin", methods=["GET", "POST"])
def adlogin():
    """Log admin in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            # return apology("must provide admin username", 403)
            flash("Invalid credentials. Please provide username.", "error")
            return render_template("adlogin.html")
        
        if request.form.get("username") != "admin":
            # return apology("Invalid ADMIN user", 403)
            flash("Invalid credentials. Please use an admin account.", "error")
            return render_template("adlogin.html")

        if not request.form.get("password"):
            # return apology("must provide admin password", 403)
            flash("Invalid credentials. Please provide a password.", "error")
            return render_template("adlogin.html")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()
        db.close()

        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            # return apology("invalid username and/or password", 403)
            flash("Invalid credentials. Invalid username/password.", "error")
            return render_template("adlogin.html")

        session["user_id"] = rows[0][0]
        
        # Hardcoded check for admin user
        if rows[0][0] == 1:  # Replace 1 with the actual hardcoded admin user ID
            session["is_admin"] = True
        else:
            session["is_admin"] = False
            
        return redirect("/")

    else:
        return render_template("adlogin.html")


@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    """Register new user"""

    if request.method == "GET":
        # In case of GET simply shows register page
        return render_template("register.html")
    else:
        # In case of POST method, Register new user

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmed password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and confirmed password match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password fields don't match", 400)

        # SQL Logic
        db = get_db()  # Assuming you have a function to get the database connection
        cursor = db.cursor()

        # Query database for username
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        rows = cursor.fetchall()

        # Ensure username is not already taken
        if len(rows) != 0:
            return apology("Username is already taken", 400)
        else:
            # In case everything is OK, register the new user and the hashed password into the DB
            cursor.execute("INSERT INTO users (username, hash) VALUES (%s, %s)", 
                           (request.form.get("username"), generate_password_hash(request.form.get("password"))))
            db.commit()  # Commit the transaction to save changes

        cursor.close()  # Close the cursor
        db.close()  # Close the database connection

        # Redirect user to login form
        return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change the password of a specified user"""
    
    if request.method == "GET":
        # In case of GET, simply show the change password page
        return render_template("edit_account.html")
    else:
        # In case of POST method, change the password

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure new password was submitted
        elif not request.form.get("password"):
            return apology("must provide new password", 400)

        # Ensure new password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm new password", 400)

        # Ensure password and confirmed password match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("new password fields don't match", 400)

        # SQL Logic
        db = get_db()  # Assuming you have a function to get the database connection
        cursor = db.cursor()

        # Check if the specified username exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (request.form.get("username"),))
        user = cursor.fetchone()

        if user is None:
            return apology("Username does not exist", 400)

        # Update the password in the database
        cursor.execute("UPDATE users SET hash = %s WHERE username = %s", 
                       (generate_password_hash(request.form.get("password")), request.form.get("username")))
        db.commit()  # Commit the transaction to save changes

        cursor.close()  # Close the cursor
        db.close()  # Close the database connection

        # Redirect user after changing the password
        return redirect("/")


@app.route("/view_accounts")
@login_required
def view_accounts():
    """View all user accounts"""

    db = get_db()  # Assuming you have a function to get the database connection
    cursor = db.cursor()

    # Fetch all users from the database
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()  # This will return a list of tuples (username, created_at)

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    # Pass the list of users to the HTML template
    return render_template("view_accounts.html", users=users)