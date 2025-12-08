SELECT 'MEM-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(membership_id, 6) AS INTEGER)) FROM memberships), 0) + 1);
UPDATE memberships SET customer_id = ?,subscription_payment_day = ?,payment_method = ?,iban = ? WHERE membership_id = ?;
INSERT INTO memberships (membership_id,customer_id,subscription_payment_day,payment_method,iban) VALUES (?,?,?,?,?);
DELETE FROM memberships WHERE membership_id = ?;

-- first script: get next id
-- second script: update user account details
-- third script: check username not within login_details
-- forth script: delete membership record