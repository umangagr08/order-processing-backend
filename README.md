# order-processing-backend

## Overview

This is a scalable backend system designed to process orders efficiently. The system supports:

- API for order creation and order status check and Metrics retrieval.
- Asynchronous order processing with worker queues.
- PostgreSQL database for persistence.
- Docker-based deployment for easy setup.

---

## Setup Instructions

### **1. Clone the Repository**

```bash
git clone https://github.com/umangagr08/order-processing-backend.git
cd order-processing-backend
```

### **2. Start the Application (Using Docker)**

```bash
sudo docker-compose up --build
```

### **3. To run the script of table creation and inserting the load to table**
#### Note: Run this below commands after your application is running.
#### PS: Password is password
```bash
psql -h localhost -U postgres -d orders_db -f schema.sql
psql -h localhost -U postgres -d orders_db -f data_population.sql
```

This will start the FastAPI app, PostgreSQL, the order processing worker and inserts the sample data to the table

---

## API Endpoints

### **Create an Order**

```bash
curl --location --request POST 'http://localhost:8000/api/v1/orders' \
--header 'Content-Type: application/json' \
--data-raw '{
    "order_id": "order123",
    "user_id": 102,
    "item_ids": [
        101,
        102,
        103
    ],
    "total_amount": 1001
}'
```

**Response:**

```json
{
    "status_code": 202,
    "message": "Order successfully processed. Please check status for order id: order123"
}
```

### **Fetch Order Details**

```bash
curl --location --request GET 'http://localhost:8000/api/v1/orders/ORD123'
```

**Response:**

```json
{
    "order_id": "ORD123",
    "status": "Completed"
}
```

### **MERTICS API**

```bash
curl --location --request GET 'http://localhost:8000/api/v1/metrics'
```

**Response:**

```json
{
    "status_code": 200,
    "message": "Succesfully fetched metrics Ddta",
    "data": {
        "total_orders_processed": 2,
        "total_processing_time": 2.0056172609329224,
        "status_counts": {
            "Pending": 0,
            "Processing": 0,
            "Completed": 2
        }
    }
}
```

---

## Design Decisions & Trade-offs

### **1. Database & Schema Design**

- PostgreSQL is used for **strong consistency**.
- `item_ids` is stored as an **array** to optimize reads.
- Indexing is applied on `status` for fast lookups.

### **2. Queue Processing & Scalability**

- Orders are queued using an **asyncio.Queue**.
- Multiple workers **consume** orders in parallel.
- Trade-off: **In-memory queues** (not persistent across restarts). Can switch to **Redis or Kafka** for persistence.

### **3. Asynchronous FastAPI**

- Async DB queries (`asyncpg`) improve performance.
- API calls are **non-blocking**, allowing concurrency.

---

## Assumptions

- Processing takes **\~2 seconds per order**.
- Only 1000 concurrent requests are coming to the server at max. Accordingly adjust workers and connection pool from config.

---

## Running Tests

To run unit tests, execute:

To simulate **1,000 concurrent orders**, run:

```bash
python load_test.py
```

---

