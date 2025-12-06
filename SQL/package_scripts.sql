SELECT 'PCK-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(package_id, 6) AS INTEGER)) FROM packages), 0) + 1);
SELECT CONCAT(package_id, " : ",name, " : ",description) FROM packages;
SELECT package_id, name, description, items_consumed, active_flag FROM packages WHERE package_id = ?;
SELECT name FROM stock WHERE part_id in (replace1);
UPDATE packages SET name = ?, description = ?, items_consumed = ?, active_flag = ? WHERE package_id = ?;
INSERT INTO packages (package_id, name, description, items_consumed, active_flag) VALUES (?,?,?,?,?);
SELECT COUNT(bk.package_id) as count_package_booked, bk.package_id as package_id, strftime('%Y-%m',bk.date_of_service) as year_month FROM bookings bk JOIN transactions tk ON bk.bookings_id = tk.booking_id GROUP BY tk.part_consumed, strftime('%Y-%m',bk.date_of_service) ORDER BY strftime('%Y-%m',bk.date_of_service);

-- first script: get next id
-- second script: get all package data
-- third script: get stock level for input package_id
-- forth script: get consumed item names using where statment of part_ids
-- fith script: update existing package record
-- sixth script: create new package record
-- seventh script: package consumption graph
