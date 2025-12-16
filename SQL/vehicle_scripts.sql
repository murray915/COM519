SELECT 'CUSVEH-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(customer_vehicle_id, 9) AS INTEGER)) FROM customer_vehicles), 0) + 1);
SELECT CONCAT(customer_vehicle_id, " : ",car_reg, " : ",car_make, " : ",car_model) FROM customer_vehicles WHERE customer_id = ?;
SELECT customer_vehicle_id, customer_id, car_reg, car_make, car_model, MOT_status, active_flag FROM customer_vehicles WHERE customer_vehicle_id = ?;
UPDATE customer_vehicles SET car_reg = ?, car_make = ?, car_model = ?, MOT_status = ?, active_flag = ? WHERE customer_vehicle_id = ?;
SELECT customer_vehicle_id,car_reg,car_make,car_model FROM customer_vehicles WHERE customer_id = ?;
SELECT cusveh.customer_vehicle_id,REPLACE(LTRIM(RTRIM(cusveh.car_reg))," ", ""),cusveh.car_make,cusveh.car_model,cusveh.active_flag FROM customer_vehicles cusveh JOIN customer cus on cus.customer_id = cusveh.customer_id JOIN users usr on usr.user_id = cus.user_id WHERE usr.user_id = ?;
INSERT INTO customer_vehicles (customer_vehicle_id,customer_id,car_reg,car_make,car_model,MOT_status,active_flag) VALUES (?,?,?,?,?,?,?);

-- first script: get next id
-- second script: get all vehicale data
-- third script: get veh data for input veh_id
-- forth script: update cust_veh details
-- fith script: get cust_veh details, input user_id
-- sixth script: create new veh