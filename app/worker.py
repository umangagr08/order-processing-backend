import asyncio
import time
import traceback
from database import Database
from logger import logger
from config import config

class OrderProcessor:
    def __init__(self):
        self.db_instance = Database()
        self.order_queue = asyncio.Queue(maxsize=config.QUEUE_MAX_SIZE)
        self._running = True
        self.num_workers = config.WORKER_COUNT

    async def process_orders(self):
        while self._running:
            order_id = await self.order_queue.get()
            start_time = time.time()

            try:
                async with self.db_instance.connection() as conn:
                    order_exists = await conn.fetchval("SELECT COUNT(*) FROM orders WHERE order_id = $1", order_id)    
                    if not order_exists:
                        logger.warning(f"Order {order_id} not found in the database. Skipping processing.")
                        continue

                # Mark order as Processing
                async with self.db_instance.connection() as conn:
                    await conn.execute("UPDATE orders SET status = 'Processing' WHERE order_id = $1", order_id)

                # Function which processes the order
                await self.order_processing_function()

                processing_time = time.time() - start_time

                # Mark order as Completed
                async with self.db_instance.connection() as conn:
                    await conn.execute(
                        "UPDATE orders SET status = 'Completed', processing_time = $1 WHERE order_id = $2",
                        processing_time, order_id
                    )

            except Exception as e:
                logger.error(f"Error processing order {order_id}: {str(e)}\n {traceback.format_exc()}")

    async def order_processing_function(self):
        await asyncio.sleep(config.SLEEP_SECONDS_FOR_ORDER_PROCESSING)  # Assume this is my processing time


    def start_processing(self):
        for _ in range(self.num_workers):
            asyncio.create_task(self.process_orders())  

    def stop_processing(self):
        self._running = False