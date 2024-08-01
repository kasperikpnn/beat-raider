CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    artist_name TEXT,
    password TEXT,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE songs (
    id TEXT PRIMARY KEY,
    user_id INT,
    name TEXT,
    genre TEXT,
    duration INT,
    likes INT DEFAULT 0,
    playcount INT DEFAULT 0,
    timestamp TIMESTAMP
);

CREATE TABLE playlists (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE playlist_songs (
    playlist_id INT REFERENCES playlists(id),
    song_id TEXT REFERENCES songs(id),
    PRIMARY KEY (playlist_id, song_id)
);

CREATE TABLE liked_songs (
    user_id INT REFERENCES users(id),
    song_id TEXT REFERENCES songs(id),
    PRIMARY KEY (user_id, song_id)
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    type TEXT,
    user_id TEXT,
    content TEXT,
    timestamp TIMESTAMP
)