import asyncio
import httpx
import random
import time

API_URL = "http://localhost:8000/api/v1/orders"

# Note: Adjust the concurrent orders count accordingly
NUM_ORDERS = 1000  # Number of concurrent orders


async def create_order(order_id):
    async with httpx.AsyncClient() as client:
        order_data = {
            "order_id": f"ORD{order_id}",
            "user_id": random.randint(100, 200),
            "item_ids": [random.randint(1, 50) for _ in range(3)],
            "total_amount": round(random.uniform(10, 100), 2),
            "status": "Pending"
        }
        try:
            response = await client.post(API_URL, json=order_data)
            return response.status_code
        except Exception as e:
            return f"Error: {e}"

async def main():
    start_time = time.time()
    
    tasks = [create_order(i) for i in range(NUM_ORDERS)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Completed {NUM_ORDERS} requests in {end_time - start_time:.2f} seconds.")
    
    success_count = results.count(202)
    failure_count = len(results) - success_count
    print(f"Success: {success_count}, Failures: {failure_count}")

if __name__ == "__main__":
    asyncio.run(main())
