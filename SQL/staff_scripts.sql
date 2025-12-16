SELECT 'STF-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(staff_id, 5) AS INTEGER)) FROM staff), 0) + 1);
SELECT * FROM STAFF WHERE user_id = ?;
SELECT 'MEC-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(mechanic_id, 5) AS INTEGER)) FROM staff), 0) + 1);
INSERT INTO staff (staff_id, user_id, staff_type, mechanic_id) VALUES (?,?,?,?);
UPDATE staff SET staff_id = ?,user_id = ?,staff_type = ?, mechanic_id = ? WHERE user_id = ?;

-- first script: get next staff id
-- second script: check if user has staff id already
-- third script: get next mech id
-- forth script: add staff id into db
-- fith script: update staff record in db