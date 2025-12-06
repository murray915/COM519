SELECT user_name FROM login_details WHERE user_id = ?;
SELECT * FROM customer_booking_data WHERE "Login Name" = ? AND date(substr("Date of Booking", 7, 4) || '-' || substr("Date of Booking", 4, 2) || '-' || substr("Date of Booking", 1, 2)) >= date('now');
SELECT * FROM customer_booking_data WHERE "Login Name" = ? AND date(substr("Date of Booking", 7, 4) || '-' || substr("Date of Booking", 4, 2) || '-' || substr("Date of Booking", 1, 2)) < date('now');

-- first script: get booking data from past, input user_name
-- second script: get booking data in the future, input user_name
-- third script: get booking data in the past, input user_name