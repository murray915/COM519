SELECT user_name FROM login_details WHERE user_id = ?;
SELECT * FROM customer_booking_data WHERE "Login Name" = ? AND (date(substr("Date of Booking", 7, 4) || '-' || substr("Date of Booking", 4, 2) || '-' || substr("Date of Booking", 1, 2)) >= date('now') AND "Status" <> 'Completed');
SELECT * FROM customer_booking_data WHERE "Login Name" = ? AND (date(substr("Date of Booking", 7, 4) || '-' || substr("Date of Booking", 4, 2) || '-' || substr("Date of Booking", 1, 2)) < date('now') OR "Status" = 'Completed');
SELECT * FROM customer_booking_display WHERE "Login Name" = ? AND date(substr("Date of Booking", 7, 4) || '-' || substr("Date of Booking", 4, 2) || '-' || substr("Date of Booking", 1, 2)) >= date('now') AND "Payment Method/Status" <> 'Cancelled';
UPDATE bookings SET date_of_service = ?, customer_vehicle_id = ? WHERE bookings_id = ?;
UPDATE bookings SET date_of_service = ?, customer_vehicle_id = ? WHERE bookings_id = ?;
UPDATE bookings SET payment_method = 'Cancellation Requested' WHERE bookings_id = ?;
INSERT INTO bookings(bookings_id,customer_id,garage_id,mechanic_id,customer_vehicle_id,referral,referral_from,package_id,date_of_service,followup_required,payment_method,paid,total_cost_net,total_cost_vat,total_cost_gross) VALUES (?,?,?,'MEC-001',?,?,?,?,?,0,'Card',0,0,0,0);
SELECT 'BK-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(bookings_id, 5) AS INTEGER)) FROM bookings), 0) + 1);

-- first script: get booking data from past, input user_name
-- second script: get booking data in the future, input user_name
-- third script: get booking data in the past, input user_name
-- forth script: get booking for window edit/display in the future, input user_name
-- fith script: update existing booking, inputs date/vech id and booking id
-- sixth script: update existing booking, inputs payment status = "Cancellation Requested", inputs booking id
-- seveth script: create new booking
-- eighth script: get next id
