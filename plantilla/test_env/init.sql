-- Create users table on compose --build
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

-- Insert an admin user into the users table
-- Hash de contrasena creado con crea_hash.py
INSERT INTO users (username, hash)
VALUES ('admin', 'scrypt:32768:8:1$40KvnmJkBV1POpGX$c3e18c57666e523b222ff38ccda81de5b71297233b9a5b2917e66c22f65666c0503309f124ea6f6467e017e18254bb3c82f569a52d431a012e20d20f8e8cdf4d');
ON CONFLICT (username) DO NOTHING;  -- Skip insert if 'admin' already exists
