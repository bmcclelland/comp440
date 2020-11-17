DROP TABLE IF EXISTS Comments;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Hobbies;
DROP TABLE IF EXISTS Follows;
DROP TABLE IF EXISTS Blogs;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    username    VARCHAR(20) NOT NULL,
    password    VARCHAR(20) NOT NULL,
    firstname   VARCHAR(30),
    lastname    VARCHAR(30),
    email       VARCHAR(254) NOT NULL,
    PRIMARY KEY (username),
    UNIQUE (email)
);

CREATE TABLE Follows (
    leader      VARCHAR(20) NOT NULL,
    follower    VARCHAR(20) NOT NULL,
    PRIMARY KEY (leader, follower),
    FOREIGN KEY (leader) REFERENCES Users (username),
    FOREIGN KEY (follower) REFERENCES Users (username)
);

CREATE TABLE Hobbies (
    username    VARCHAR(20) NOT NULL,
    hobby       VARCHAR(50) NOT NULL,
    PRIMARY KEY (username, hobby),
    FOREIGN KEY (username) REFERENCES Users (username)
);

CREATE TABLE Blogs (
    blogid      INT NOT NULL AUTO_INCREMENT,
    subject     VARCHAR(50) NOT NULL,
    description VARCHAR(250),
    postuser    VARCHAR(20) NOT NULL,
    pdate       DATE NOT NULL,
    PRIMARY KEY (blogid),
    FOREIGN KEY (postuser) REFERENCES Users (username)
);

CREATE TABLE Tags (
    blogid  INT NOT NULL,
    tag     VARCHAR(20) NOT NULL,
    PRIMARY KEY (blogid, tag),
    FOREIGN KEY (blogid) REFERENCES Blogs (blogid)
);

CREATE TABLE Comments (
    commentid   INT NOT NULL AUTO_INCREMENT,
    sentiment   VARCHAR(20) NOT NULL,
    description VARCHAR(250) NOT NULL,
    cdate       DATE NOT NULL,
    blogid      INT NOT NULL,
    author      VARCHAR (20) NOT NULL,
    PRIMARY KEY (commentid),
    FOREIGN KEY (blogid) REFERENCES Blogs (blogid),
    FOREIGN KEY (author) REFERENCES Users (username)
);
