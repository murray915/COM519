SELECT 'CUS-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(customer_id, 6) AS INTEGER)) FROM customer), 0) + 1);
SELECT customer_id, user_id FROM customer WHERE user_id = ?;
INSERT INTO customer(customer_id, user_id) VALUES (?,?);

-- first script: get next customer_id
-- second script: create customer_id for user_id