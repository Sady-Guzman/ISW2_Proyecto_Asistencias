from werkzeug.security import generate_password_hash

# Replace 'your_password_here' with the desired password for the admin user
password = "domino"
hashed_password = generate_password_hash(password)

print(f"Hashed password: {hashed_password}")
