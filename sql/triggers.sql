DROP TRIGGER IF EXISTS CheckBlog;
DROP TRIGGER IF EXISTS CheckComment;

/* Each trigger raises a unique signal for the server to handle. */

CREATE TRIGGER CheckBlog BEFORE INSERT ON Blogs FOR EACH ROW BEGIN
    /* A user cannot post more than 2 blogs per day. */
    IF 2 <= (SELECT count(*) FROM Blogs WHERE author=NEW.author AND blogdate=NEW.blogdate)
        THEN SIGNAL SQLSTATE '99001';
    END IF;
END;

CREATE TRIGGER CheckComment BEFORE INSERT ON Comments FOR EACH ROW BEGIN
    /* A user cannot post more than 3 comments per day. */
    IF 3 <= (SELECT count(*) FROM Comments WHERE author=NEW.author AND commentdate=NEW.commentdate)
        THEN SIGNAL SQLSTATE '99002';
    /* A user cannot post more than 1 comment per blog. */
    ELSEIF 1 <= (SELECT count(*) FROM Comments WHERE author=NEW.author AND blogid=NEW.blogid)
        THEN SIGNAL SQLSTATE '99003';
    /* A user cannot comment on their own blog. */
    ELSEIF 0 < (SELECT count(*) FROM Blogs WHERE blogid=NEW.blogid AND author=NEW.author)
        THEN SIGNAL SQLSTATE '99004';
    END IF;
END;
