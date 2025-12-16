SELECT * FROM staff_booking_display WHERE "Garage ID" = ? AND "Status" <> "Completed";
SELECT 'TACT-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(transaction_id, 6) AS INTEGER)) FROM transactions), 0) + 1);
UPDATE bookings SET date_of_service = ? WHERE bookings_id = ?;
UPDATE bookings SET payment_method = 'Cancelled', paid = 1, total_cost_net = 0,total_cost_vat = 0,total_cost_gross = 0 WHERE bookings_id = ?;
SELECT package_id, name, description, items_consumed, active_flag, item_qty_consumed FROM packages WHERE package_id = ?;
SELECT pk.items_consumed, pk.item_qty_consumed, bk.customer_vehicle_id FROM packages pk JOIN bookings bk on pk.package_id = bk.package_id WHERE bk.bookings_id = ?;
SELECT part_id, replace1 FROM stock WHERE part_id in (replace2);
UPDATE bookings SET paid = 1, total_cost_net = ?,total_cost_vat = ?,total_cost_gross = ? WHERE bookings_id = ?;
INSERT INTO transactions (transaction_id, booking_id, customer_vehicle_id, part_consumed, qty_consumed) VALUES replace;
UPDATE stock SET replace = ? WHERE part_id = ?;

-- first script: get display booking info
-- second script: get next transaction id
-- third script: update booking date
-- forth script: update booking for cancellation
-- fith script: grab QTY package data
-- sixth script: get item list from booking_id input
-- seventh script: get part QTY and Stock levels for part_id list input
-- eight script: update booking_id to complete. Input booking_id
-- ninth script: insert new transaction records
-- tenth script: update stock level for part_id input

