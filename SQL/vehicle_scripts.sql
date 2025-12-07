SELECT 'CUSVEH-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(customer_vehicle_id, 9) AS INTEGER)) FROM customer_vehicles), 0) + 1);
SELECT CONCAT(customer_vehicle_id, " : ",car_reg, " : ",car_make, " : ",car_model) FROM customer_vehicles WHERE customer_id = ?;
SELECT customer_vehicle_id, customer_id, car_reg, car_make, car_model, MOT_status, active_flag FROM customer_vehicles WHERE customer_vehicle_id = ?;
UPDATE customer_vehicles SET car_reg = ?, car_make = ?, car_model = ?, MOT_status = ?, active_flag = ? WHERE customer_vehicle_id = ?;
--INSERT INTO packages (package_id, name, description, items_consumed, active_flag) VALUES (?,?,?,?,?);
--SELECT COUNT(bk.package_id) as count_package_booked, bk.package_id as package_id, strftime('%Y-%m',bk.date_of_service) as year_month FROM bookings bk JOIN transactions tk ON bk.bookings_id = tk.booking_id GROUP BY tk.part_consumed, strftime('%Y-%m',bk.date_of_service) ORDER BY strftime('%Y-%m',bk.date_of_service);


-- first script: get next id
-- second script: get all vehicale data
-- third script: get veh data for input veh_id
-- forth script: update cust_veh details


-- fith script: update existing package record
-- sixth script: create new package record
-- seventh script: package consumption graph