SELECT 'TACT-' || printf('%03d',COALESCE((SELECT MAX(CAST(substr(transaction_id, 6) AS INTEGER)) FROM transactions), 0) + 1);


-- first script: get next transaction id
-- second script: get garage id from user acc