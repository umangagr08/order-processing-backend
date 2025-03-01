import traceback
from fastapi import APIRouter, Request

from fastapi.responses import JSONResponse
from marshmallow import ValidationError
from database import Database
from models import OrderSchema, OrderStatusResponseSchema
from logger import logger

db_instance = Database()
router = APIRouter()

def get_order_queue():
    from app.main import order_queue  # Delayed import
    return order_queue

@router.post("/orders")
async def create_order(request: Request):
    try:
        order_data = await request.json()
        order_schema = OrderSchema()
        validated_data = order_schema.load(order_data)

        order_id = validated_data["order_id"]

        async with db_instance.connection() as conn:
            # Check if order already exists
            existing_order = await conn.fetchval(
                "SELECT COUNT(*) FROM orders WHERE order_id = $1",
                order_id
            )
            if existing_order:
                return JSONResponse(
                    status_code=400,
                    content={
                        "status_code": 400,
                        "message": f"Order with order_id {order_id} already exists."
                    }
                )

        async with db_instance.connection() as conn:
            await conn.execute(
                "INSERT INTO orders (order_id, user_id, item_ids, total_amount, status) VALUES ($1, $2, $3::INTEGER[], $4, 'Pending')",
                order_id, validated_data["user_id"], validated_data["item_ids"], validated_data["total_amount"]
            )

        order_queue = get_order_queue()
        await order_queue.put(order_id)

        return JSONResponse(
            status_code=202,
            content={
                "status_code": 202,
                "message": f"Order successfully processed. Please check status for order id: {order_id}"
            }
        )
    except ValidationError as e:
        logger.error(f"Validation Error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "status_code": 400,
                "message": "Validation Error"
            }
        )
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}:\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "status_code": 500,
                "message": "Internal Server Error!"
            }
        )    

@router.get("/orders/{order_id}")
async def get_order_status(order_id: str):
    try:
        async with db_instance.connection() as conn:
            result = await conn.fetchrow("SELECT status FROM orders WHERE order_id = $1", order_id) 
        if not result:
            logger.warning(f"Order not found: {order_id}")
            return JSONResponse(
                status_code=404,
                content={
                    "status_code": 404,
                    "message": "Order not found"
                }
            )
        response_data = OrderStatusResponseSchema().dump({"order_id": order_id, "status": result[0]})
        return JSONResponse(
            status_code=200,
            content=response_data
        ) 
    except Exception as e:
        logger.error(f"Error fetching order status: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "status_code": 500,
                "message": "Internal Server Error"
            }
        )

@router.get("/metrics")
async def get_metrics():
    try:
        async with db_instance.connection() as conn:
            pending_orders = await conn.fetchval("SELECT COUNT(*) FROM orders WHERE status = 'Pending'")
            processing_orders = await conn.fetchval("SELECT COUNT(*) FROM orders WHERE status = 'Processing'")
            completed_orders = await conn.fetchval("SELECT COUNT(*) FROM orders WHERE status = 'Completed'")

            total_orders_processed = completed_orders + processing_orders + pending_orders

            # Calculate average processing time from DB
            avg_processing_time = await conn.fetchval(
                "SELECT AVG(processing_time) FROM orders WHERE status = 'Completed'"
            )
            avg_processing_time = avg_processing_time if avg_processing_time else 0

        metrics_data = {
            "total_orders_processed": total_orders_processed,
            "total_processing_time": avg_processing_time,
            "status_counts": {
                "Pending": pending_orders,
                "Processing": processing_orders,
                "Completed": completed_orders
            }
        }
        return JSONResponse(
            status_code=200,
            content={
                "status_code": 200,
                "message": "Succesfully fetched metrics Ddta",
                "data": metrics_data
            }
        )
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "status_code": 500,
                "message": "Internal Server Error!"
            }
        )