from werkzeug.security import generate_password_hash

# Este archivo no se usa en la implementacion, Es util tenerlo para probar la funcion de la libreria werkzeug
# Se us'o para generar hash de contrasena admin

# string para hashear.
password = "hospital"
hashed_password = generate_password_hash(password)

print(f"Hashed password: {hashed_password}")
