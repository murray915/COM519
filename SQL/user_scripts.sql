SELECT 'USR-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(user_id, 6) AS INTEGER)) FROM users), 0) + 1);
SELECT usr.user_id,usr.name,usr.address,pst.postcode,usr.email,usr.phone_no,usr.primary_garage,usr.access_code,usr.active_flag,ld.user_name,mbs.membership_id,mbs.customer_id,mbs.subscription_payment_day,mbs.payment_method,mbs.iban FROM users usr JOIN postcodes pst ON usr.postcode_id = pst.postcode_id JOIN login_details ld ON usr.user_id = ld.user_id JOIN customer cus ON cus.user_id = usr.user_id LEFT JOIN memberships mbs ON cus.customer_id = mbs.customer_id WHERE usr.user_id = ?;
UPDATE users SET name= ?, address = ?, postcode_id = ?, email = ?, phone_no = ?, primary_garage = ? WHERE user_id = ?;
SELECT ld.user_name FROM login_details ld WHERE ld.user_name = ?;
SELECT CONCAT(ld.user_id, " : ",ld.user_name, " : ",usr.name) FROM login_details as ld JOIN users usr ON usr.user_id = ld.user_id;
SELECT usr.user_id,usr.access_code,usr.active_flag,ld.user_name FROM users usr JOIN login_details ld ON usr.user_id = ld.user_id WHERE usr.user_id = ?;
SELECT CONCAT(access_code," : ",description) FROM access_codes;
UPDATE users SET access_code = ?,active_flag = ? WHERE user_id = ?;
UPDATE login_details SET password = ? WHERE user_id = ?;


-- first script: get next id
-- second script: get user data, including membership
-- third script: update user account details
-- forth script: check username not within login_details
-- fith script: get user account data for dropdowns
-- sixth script: get user account information for backing data
-- seventh script: access code data
-- eighth script: update user details from ADMIN funcs
-- ninth script: update login_details from ADMIN funcs
