class Config:
    WORKER_COUNT = 3 
    DATABASE_URL = "postgresql://postgres:password@localhost/orders_db"
    QUEUE_MAX_SIZE = 100
    SLEEP_SECONDS_FOR_ORDER_PROCESSING = 2
    POOL_MIN_SIZE = 10
    POOL_MAX_SIZE = 100
    POSTGRES_USER = "postgres"
    POSTGRES_PASS = "password"
    POSTGRES_HOST = "db"
    POSTGRES_DB = "orders_db"

config = Config()