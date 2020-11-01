DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username VARCHAR(32) PRIMARY KEY,
    password VARCHAR(32)
);

INSERT INTO users (username,password) VALUES
    ('alice','aaa'),
    ('bob','bbb'),
    ('charlie','ccc'),
    ('david','ddd'),
    ('eve','eee');
