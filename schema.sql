CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE songs (
    id TEXT,
    user_id TEXT,
    name TEXT,
    genre TEXT,
    timestamp TIMESTAMP
)