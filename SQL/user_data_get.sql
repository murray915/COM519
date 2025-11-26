--check username not within login_details
SELECT 

ld.user_name

FROM login_details ld

WHERE ld.user_name = ?;