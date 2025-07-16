-- Création des tables
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    filepath VARCHAR(255) NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Hash générés avec werkzeug pour alicepass et bobpass (une seule ligne chacun)
INSERT INTO users (id, username, password_hash) VALUES
    (1, 'alice', 'scrypt:32768:8:1$knqTxDVFMgRAv5b7$ecc7749d4f97410a9109e9e01f74c013c643b4a9ffe66799c18f2374def747f9c8b4f7ab9c58b70eb19dc0e627a09158f6c362744d3c44fed6887b377b52066e'),
    (2, 'bob', 'scrypt:32768:8:1$XdYgm6f7hzR106mW$242739f1b3776b69815b7b41ceee5c43ba1531fd462502a29bb6336a3a2ce04d51d05947ab9b6b5fa1ee268ef234c02158bbf20a2e8e3ea01ece5fb908547173');

-- Seed document appartenant à bob (id=2)
INSERT INTO documents (id, user_id, filename, filepath) VALUES
    (42, 2, 'confidential-bob.pdf', '/app/uploads/confidential-bob.pdf'); 