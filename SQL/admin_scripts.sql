SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
PRAGMA table_info(replace);
INSERT INTO replace0(replace1) VALUES (replace2);

-- first script: get all tables
-- second script: get table names
-- third script: mass import of values, table name and values to be passed