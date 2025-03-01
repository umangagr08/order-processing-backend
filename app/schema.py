from database import Database

async def initialize_database():
    db_instance = Database()

    try:
        async with db_instance.connection() as conn:

            # Create orders table if it doesn't exist
            await conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                item_ids INTEGER[] NOT NULL,
                total_amount REAL NOT NULL CHECK (total_amount >= 0),
                status TEXT CHECK(status IN ('Pending', 'Processing', 'Completed')) DEFAULT 'Pending',
                processing_time REAL DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Creates an Index on status field for faster quering
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);")

            print("Database initialized successfully with indexes!")
    
    except Exception as e:
        print(f"Error initializing database: {e}")