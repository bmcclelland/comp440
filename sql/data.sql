INSERT INTO Users (username,password,email,firstname,lastname) VALUES
    ('alice','aaa','alice@email.com', 'Alice', 'A'),
    ('bob','bbb', 'bob@email.com', 'Bob', 'B'),
    ('charlie','ccc', 'charlie@email.com', 'Charlie', 'C'),
    ('david','ddd', 'david@email.com', 'David', 'D'),
    ('eve','eee','eve@email.com', 'Eve', 'E');

INSERT INTO Follows (leader, follower) VALUES
    ('alice', 'bob'),
    ('alice', 'charlie'),
    ('alice', 'david'),
    ('alice', 'eve'),
    ('bob', 'charlie'),
    ('bob', 'eve'),
    ('charlie', 'bob'),
    ('charlie', 'eve'),
    ('david', 'eve');

INSERT INTO Hobbies (username, hobby) VALUES
    ('alice', 'movie'),
    ('alice', 'swimming'),
    ('bob', 'bowling'),
    ('bob', 'cooking'),
    ('david', 'calligraphy'),
    ('david', 'dancing'),
    ('david', 'movie'),
    ('eve', 'hiking'),
    ('eve', 'swimming');

INSERT INTO Blogs (author, blogdate, subject, description) VALUES
    ('eve',     '2019-09-10', "First post",      'Something'),
    ('david',   '2020-01-01', "2020",            'Happy new year'),
    ('alice',   '2020-01-01', "New year",        'Happy new year'),
    ('eve',     '2020-09-10', "One year later",  'Stuff'),
    ('alice',   '2020-10-10', "Got a dog",       "This dog is cute"),
    ('bob',     '2020-10-10', "SQL Tutorial",    'SELECT * FROM table;');

INSERT INTO Tags (blogid,tag) VALUES
    (3, "New Year"),
    (3, "2020"),
    (5, "dogs"),
    (5, "pets"),
    (6, "SQL"),
    (6, "Databases"),
    (2, "2020");

INSERT INTO Comments (blogid, author, commentdate, sentiment, description) VALUES
    (1, 'alice',   '2019-09-09', 'negative', "Nope"),
    (3, 'david',   '2020-01-01', 'positive', "You too"),
    (3, 'eve',     '2020-01-01', 'positive', "Happy new year"),
    (5, 'charlie', '2020-11-07', 'negative', "I don't like dogs"),
    (6, 'charlie', '2020-11-15', 'negative', "Not helpful"),
    (6, 'alice',   '2020-11-20', 'positive', "Very helpful");
