import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

from fastapi import FastAPI
from database import Database
from api import router as api_router
from worker import OrderProcessor
from schema import initialize_database

app = FastAPI()

# Database Initialization
db_instance = Database()
order_processor = OrderProcessor()
order_queue = order_processor.order_queue

@app.on_event("startup")
async def startup_event():
    """Initialize db and start processing orders when the app starts."""
    await db_instance.init_db()
    await initialize_database()
    order_processor.start_processing()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop processing orders when the app shuts down."""
    order_processor.stop_processing()


# Include API Routes
app.include_router(api_router, prefix="/api/v1")

