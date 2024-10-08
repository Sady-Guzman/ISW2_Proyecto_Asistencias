from werkzeug.security import generate_password_hash

# string para hashear.
# Dejar esto en .gitignore mas adelante
password = "domino"
hashed_password = generate_password_hash(password)

print(f"Hashed password: {hashed_password}")
