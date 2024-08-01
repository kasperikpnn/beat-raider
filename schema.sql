CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    artist_name TEXT,
    password TEXT
);

CREATE TABLE songs (
    id TEXT,
    user_id TEXT,
    name TEXT,
    genre TEXT,
    timestamp TIMESTAMP
)

CREATE TABLE messages (
    type TEXT,
    user_id TEXT,
    content TEXT,
    timestamp TIMESTAMP
)