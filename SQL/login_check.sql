--check user login details and return user details if valid
SELECT 

ld.user_id
,ud.name
,ud.address
,pc.postcode
,ud.email
,ud.phone_no
,ud.access_code

FROM login_details ld
    JOIN users ud
        ON ld.user_id = ud.user_id
    JOIN postcodes pc
        ON ud.postcode_id = pc.postcode_id

WHERE (ld.user_name = ?
    AND ld.password = ?)
    AND ud.active_flag = 1;