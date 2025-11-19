SELECT
   
   CASE 
       WHEN CAST(SUBSTRING(user_id,instr(user_id,'-')+1,3) as int) +1 <= 9 THEN concat('user-00', CAST(SUBSTRING(user_id,instr(user_id,'-')+1,3) as int)+1)
       WHEN CAST(SUBSTRING(user_id,instr(user_id,'-')+1,3) as int) +1 >= 10 and CAST(SUBSTRING(user_id,instr(user_id,'-')+1,3) as int) +1 <= 99 THEN concat('user-0', CAST(SUBSTRING(user_id,instr(user_id,'-')+1,3) as int)+1)
       WHEN CAST(SUBSTRING(user_id,instr(user_id,'-')+1,3) as int) +1 >= 100 and CAST(SUBSTRING(user_id,instr(user_id,'-')+1,3) as int) +1 <= 999 THEN concat('user-00', CAST(SUBSTRING(user_id,instr(user_id,'-')+1,3) as int)+1)
           else 'ERR'
       End as 'Rowref'
       
FROM users
ORDER BY user_id DESC
LIMIT(1);