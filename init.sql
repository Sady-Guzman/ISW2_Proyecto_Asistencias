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
INSERT INTO users (rut, username, hash) VALUES ('0000000-0', 'admin', 'scrypt:32768:8:1$LXDOuJgd9ALS4Pba$3b221f58e00a35fecdc1383b32f1038334d1ca9992a8c5a97f46dad07476945826f7c6c246f00e745fcec395f9e64daaacc14a437f996b5e95174b792b064632') ON CONFLICT (username) DO NOTHING;  -- Skip insert if 'admin' already exists
