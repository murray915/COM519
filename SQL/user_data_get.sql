--check username not within login_details
SELECT 

ud.user_name

FROM login_details ld

WHERE ld.user_name = ?;