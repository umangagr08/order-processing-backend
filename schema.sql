-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    item_ids INTEGER[] NOT NULL,
    total_amount REAL NOT NULL CHECK (total_amount >= 0),
    status TEXT CHECK(status IN ('Pending', 'Processing', 'Completed')) DEFAULT 'Pending',
    processing_time REAL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);