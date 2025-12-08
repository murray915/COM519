SELECT 'USR-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(user_id, 6) AS INTEGER)) FROM users), 0) + 1);
SELECT usr.user_id,usr.name,usr.address,pst.postcode,usr.email,usr.phone_no,usr.primary_garage,usr.access_code,usr.active_flag,ld.user_name,mbs.membership_id,mbs.customer_id,mbs.subscription_payment_day,mbs.payment_method,mbs.iban FROM users usr JOIN postcodes pst ON usr.postcode_id = pst.postcode_id JOIN login_details ld ON usr.user_id = ld.user_id JOIN customer cus ON cus.user_id = usr.user_id LEFT JOIN memberships mbs ON cus.customer_id = mbs.customer_id WHERE usr.user_id = ?;
UPDATE users SET name= ?, address = ?, postcode_id = ?, email = ?, phone_no = ?, primary_garage = ? WHERE user_id = ?;

-- first script: get next id
-- second script: get user data, including membership
-- third script: update user account details
