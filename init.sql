CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    rut CHAR(11) NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

-- NOTAS SOBRE RUT!
-- Se tiene considerado RUT con formato: NO PUNTOS, CON GUION
-- RUT no es unico, para permitir un mismo trabajador usar cuentas distintas en caso de que haga funciones distintas

-- Insert an admin user
-- Hash de contrasena creado con crea_hash.py
INSERT INTO users (rut, username, hash)
VALUES ('0000000-0', 'admin', 'scrypt:32768:8:1$zVWQjQRhaG6fNVVO$23fab2ec89b38b65d0a403f368b8a679c0b103e1b295a82b2c56f93287f9d05ff70f9e9a5c726feb54049c160e89f01a3716d98e5f6b4b51ec86cec170b26dca')
ON CONFLICT (username) DO NOTHING;  -- Skip insert if 'admin' already exists

-- Insert Test User para pasar pruebas 
INSERT INTO users (rut, username, hash)
VALUES ('0000000-1', 'tuser', 'scrypt:32768:8:1$lP3LAjkFbOLzgYry$a8ef3ac7467d00dec69b77eff14b4bdd2b407dd8f1df37f20e9216578ec730e91cab923d06c2e3a1a6555356bfcd907413b148c1e93b9a66a8bf30543205b238')
ON CONFLICT (username) DO NOTHING;  -- Skip insert if 'tuser' (test user) already exists