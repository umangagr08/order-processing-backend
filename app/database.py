from contextlib import asynccontextmanager
import asyncpg
from threading import Lock
from config import config

class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._db_pool = None
        return cls._instance

    async def init_db(self):
        if self._db_pool is None:
            self._db_pool = await asyncpg.create_pool(
                dsn=(
                    f"postgresql://{config.POSTGRES_USER}:"
                    f"{config.POSTGRES_PASS}@"
                    f"{config.POSTGRES_HOST}/"
                    f"{config.POSTGRES_DB}"
                ),
                min_size=config.POOL_MIN_SIZE,
                max_size=config.POOL_MAX_SIZE
            )

    @asynccontextmanager
    async def connection(self):
        """Async context manager to acquire and release a connection."""
        if self._db_pool is None:
            raise Exception("Database connection pool is not initialized.")
        
        conn = await self._db_pool.acquire()
        try:
            yield conn
        finally:
            await self._db_pool.release(conn)