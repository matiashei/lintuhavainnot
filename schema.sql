CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    species TEXT,
    date DATE,
    amount INTEGER,
    place TEXT,
    municipality TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    image BLOB
);