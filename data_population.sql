-- Insert sample orders
INSERT INTO orders (order_id, user_id, item_ids, total_amount, status, processing_time)
VALUES 
    ('ORD111', 101, ARRAY[1, 2, 3], 49.99, 'Pending', NULL),
    ('ORD112', 102, ARRAY[4, 5], 29.99, 'Processing', NULL),
    ('ORD113', 103, ARRAY[6, 7, 8], 99.99, 'Completed', 2.5),
    ('ORD114', 104, ARRAY[9, 10], 59.99, 'Pending', NULL),
    ('ORD115', 105, ARRAY[11, 12, 13], 79.99, 'Completed', 3.1);
