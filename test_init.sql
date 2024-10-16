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

-- pass for testuser: 123
INSERT INTO users (username, hash)
VALUES ('testuser', 'scrypt:32768:8:1$dKawgYqCtsqGFynq$dc09dcb7ef301d1c5f710197345fd63b421a8567997d3ecd41164e17e733d9354220e28a93b5ed01e6c0f56c9903cc17505d81fb5640acf5818cdc5cf2900fd3');
ON CONFLICT (username) DO NOTHING;  -- Skip insert if 'testuser' already exists
