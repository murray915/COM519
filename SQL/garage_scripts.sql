SELECT 'GRDG-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(garage_id, 6) AS INTEGER)) FROM garages), 0) + 1);
SELECT CONCAT(garage_id, " : ",name, " : ",address) FROM garages;
SELECT part_id, name, description, replace1 FROM stock WHERE part_id = ?;
UPDATE stock SET replace1 = ? WHERE part_id = ?;


-- first script: get next id
-- second script: get all garages ids & data
-- third script: get stock level for input part_id. replace1 is garage_id
-- forth script: update stock level from garage_id / part_id input(s)
