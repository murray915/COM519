SELECT 'USR-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(user_id, 6) AS INTEGER)) FROM users), 0) + 1);
SELECT usr.user_id,usr.name,usr.address,pst.postcode,usr.email,usr.phone_no,usr.primary_garage,usr.access_code,usr.active_flag FROM users usr JOIN postcodes pst ON usr.postcode_id = pst.postcode_id WHERE user_id = ?;
UPDATE users SET name= ?, address = ?, postcode_id = ?, email = ?, phone_no = ?, primary_garage = ? WHERE user_id = ?;

-- first script: get next id
-- second script: get user data
-- third script: update user account details
