SELECT 'GRDG-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(garage_id, 6) AS INTEGER)) FROM garages), 0) + 1);
SELECT CONCAT(garage_id, " : ",name, " : ",address) FROM garages;
SELECT part_id, name, description, replace1 FROM stock WHERE part_id = ?;
UPDATE stock SET replace1 = ? WHERE part_id = ?;
SELECT grg.garage_id,grg.name,grg.address,pst.postcode,grg.email,grg.phone_number,grg.contact_staff FROM garages as grg JOIN postcodes pst ON pst.postcode_id = grg.postcode_id WHERE grg.garage_id = ?;
UPDATE garages SET name = ?,address = ?,postcode_id = ?,email = ?,phone_number = ?,contact_staff = ? WHERE garage_id = ?;
INSERT INTO garages (garage_id,name,address,postcode_id,email,phone_number,contact_staff) VALUES (?,?,?,?,?,?,?);
ALTER TABLE stock ADD COLUMN replace INTEGER DEFAULT 0;
SELECT usr.primary_garage FROM users usr JOIN login_details ld ON usr.user_id = ld.user_id LEFT JOIN staff st ON st.user_id = usr.user_id WHERE usr.user_id = ?;

-- first script: get next id
-- second script: get all garages ids & data
-- third script: get stock level for input part_id. replace1 is garage_id
-- forth script: update stock level from garage_id / part_id input(s)
-- fith script: get all garage data for an input id
-- sixth script: update garage record
-- seventh script: create a new garage record
-- eigth script: create new column in stock table for new garage
-- ninth script: get prime garages ids & data (based on primary garage)
