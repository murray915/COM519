SELECT 'PST-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(postcode_id, 5) AS INTEGER)) FROM postcodes), 0) + 1);
SELECT postcode_id FROM postcodes WHERE postcode LIKE ?;
INSERT INTO postcodes (postcode_id, postcode) VALUES (?,?);

-- first script: get next postcode_id
-- second script: check postcode input has id
-- third script: create postcode record from input