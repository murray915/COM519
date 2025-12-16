SELECT part_id, name, description, common_repair_group, image, active_flag FROM stock WHERE part_id =?;
SELECT CONCAT(part_id, " : ",name, " : ",description) FROM stock;
PRAGMA table_info(stock);
SELECT 'ITM-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(part_id, 5) AS INTEGER)) FROM stock), 0) + 1);
INSERT INTO stock (replace1) VALUES (replace2);
SELECT COUNT(tk.part_consumed) as qty_consumed, tk.part_consumed as part_id, strftime('%Y-%m',bk.date_of_service) as year_month FROM bookings bk JOIN transactions tk ON bk.bookings_id = tk.booking_id GROUP BY tk.part_consumed, strftime('%Y-%m',bk.date_of_service) HAVING COUNT(tk.part_consumed) > 0 AND strftime('%Y-%m', bk.date_of_service) >= '2022-01' ORDER BY strftime('%Y-%m',bk.date_of_service)

-- first script: get stock data for frame 1 display
-- second script: get all item ids
-- third script: get all column names
-- forth script: get next id
-- fith script: insert/create new item. replace1/replace2 inserting tables/values
-- Sixth script: consumption data for items for info frame
