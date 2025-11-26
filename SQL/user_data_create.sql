SELECT 'USR-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(user_id, 5) AS INTEGER)) FROM users), 0) + 1);
INSERT INTO users(user_id, name, address, postcode_id, email, phone_no, primary_garage, access_code, account_creation_date, active_flag) VALUES (?,?,?,?,?,?,'N/A','CUS_USR',current_date,1);
INSERT INTO login_details(user_id, user_name, password) VALUES (?,?,?);
SELECT ud.user_id,ld.user_name FROM login_details ld JOIN users ud ON ld.user_id = ud.user_id WHERE ud.user_id = ?;

-- first script: get next user_id
-- second script: create user record from inputs
-- third script: create login_details record (username/pass) from inputs
-- forth script: search newly created data