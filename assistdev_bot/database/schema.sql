CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    full_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    service_name TEXT,
    service_price INTEGER,
    extra_package TEXT,
    extra_price INTEGER DEFAULT 0,
    total_price INTEGER,
    client_name TEXT,
    contact TEXT,
    details TEXT,
    status TEXT DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);