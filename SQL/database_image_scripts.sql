SELECT image FROM stock WHERE part_id=?;
UPDATE stock SET image = ? WHERE part_id=?;

-- first script: get blob data from database
-- second script: update record with image