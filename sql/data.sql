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
    ('alice',   '2020-01-01', "New year",        'Happy new year'),
    ('alice',   '2020-10-10', "Got a dog",       "This dog is cute"),
    ('bob',     '2020-10-15', "SQL Tutorial",    'SELECT * FROM table;'),
    ('david',   '2020-01-01', "2020",            'Happy new year'),
    ('eve',     '2019-09-10', "First post",      'Something'),
    ('eve',     '2020-09-10', "One year later",  'Stuff');

INSERT INTO Tags (blogid,tag) VALUES
    (1, "New Year"),
    (1, "2020"),
    (2, "dogs"),
    (2, "pets"),
    (3, "SQL"),
    (3, "Databases"),
    (4, "2020");

INSERT INTO Comments (blogid, author, commentdate, sentiment, description) VALUES
    (1, 'david',   '2020-01-01', 'positive', "You too"),
    (1, 'eve',     '2020-01-01', 'positive', "Happy new year"),
    (2, 'charlie', '2020-11-07', 'negative', "I don't like dogs"),
    (3, 'charlie', '2020-11-15', 'negative', "Not helpful"),
    (3, 'alice',   '2020-11-20', 'positive', "Very helpful");
