import mysql.connector

class ErrorBlogsPerDay:
    pass

class ErrorCommentsPerDay:
    pass

class ErrorCommentsPerBlog:
    pass

class ErrorCommentOwnBlog:
    pass

def insert_user(username, password, email, firstname, lastname):
    firstname = _fixup_name(firstname)
    lastname  = _fixup_name(lastname)
    db = _connect()
    cursor = db.cursor()
    try:
        query = "INSERT INTO Users (username, password, email, firstname, lastname) VALUES (%s, %s, %s, %s, %s)"
        data = (username, password, email, firstname, lastname)
        cursor.execute(query, data)
        db.commit()
    finally:
        cursor.close()
        db.close()

def verify_user(usernameStr, passwordStr):
    db = _connect()
    cursor = db.cursor()
    try:
        query = "SELECT username FROM Users WHERE username = %s and password = %s"
        data = (usernameStr, passwordStr)
        cursor.execute(query, data)
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        db.close()

def verify_free_username(username):
    db = _connect()
    cursor = db.cursor()
    try:
        query = "SELECT username FROM Users WHERE username = %s"
        data = (username,)
        cursor.execute(query, data)
        return cursor.fetchone() is None
    finally:
        cursor.close()
        db.close()

def verify_free_email(email):
    db = _connect()
    cursor = db.cursor()
    try:
        query = "SELECT email FROM Users WHERE email = %s"
        data = (email,)
        cursor.execute(query, data)
        return cursor.fetchone() is None
    finally:
        cursor.close()
        db.close()

def get_bloglist():
    db = _connect()
    cursor = db.cursor(dictionary=True)
    try:
        query = """
            SELECT B.blogid as id, B.author, B.subject, B.blogdate as date, U.firstname, U.lastname
            FROM Blogs as B, Users as U
            WHERE B.author = U.username
            ORDER BY B.blogdate DESC, B.blogid DESC
        """
        cursor.execute(query)
        return map(_join_names, cursor.fetchall())
    finally:
        cursor.close()
        db.close()

def create_blog(author, subject, description, tags):
    db = _connect()
    cursor = db.cursor()
    try:
        # Insert blog
        query = "INSERT INTO Blogs (author, subject, description, blogdate) VALUES (%s, %s, %s, NOW())"
        data = (author, subject, description)
        cursor.execute(query, data)
        # Insert tags
        blogid = cursor.lastrowid
        for tag in tags:
            query = "INSERT INTO Tags (blogid, tag) VALUES (%s, %s)"
            data = (blogid, tag)
            cursor.execute(query, data)
        # Commit
        db.commit()
        return None # No error
    except mysql.connector.Error as err:
        if err.sqlstate == '99001':
            return ErrorBlogsPerDay()
        else:
            raise
    finally:
        cursor.close()
        db.close()

def create_comment(blogid, author, sentiment, description):
    db = _connect()
    cursor = db.cursor()
    try:
        query = "INSERT INTO Comments (blogid, author, sentiment, description, commentdate) VALUES (%s, %s, %s, %s, NOW())"
        data = (blogid, author, sentiment, description)
        cursor.execute(query, data)
        db.commit()
        return None # No error
    except mysql.connector.Error as err:
        if err.sqlstate == '99002':
            return ErrorCommentsPerDay()
        elif err.sqlstate == '99003':
            return ErrorCommentsPerBlog()
        elif err.sqlstate == '99004':
            return ErrorCommentOwnBlog()
        else:
            raise
    finally:
        cursor.close()
        db.close()

# Strips bordering whitespace, returns None if name is all whitespace or empty
def _fixup_name(name):
    name = name.strip()
    if not name:
        return None
    else:
        return name

# Join firstname/lastname together, respecting Nones
def _join_names(item):
    firstname = item.pop('firstname')
    lastname  = item.pop('lastname')
    fullname = None

    if firstname is None:
        fullname = lastname
    elif lastname is None:
        fullname = firstname
    else:
        fullname = firstname + ' ' + lastname

    item['fullname'] = fullname
    return item

def _unwrap_singles(xs):
    result = []
    for (x,) in xs:
        result.append(x)
    return result

def get_blog(blogid):
    # Returns the given blog along with its tags and comments.
    # If no such blog, return None.
    db = _connect()
    cursor = db.cursor(dictionary=True)
    try:
        # Get blog
        query = """
            SELECT B.blogid as id, B.author, B.subject, B.description, B.blogdate as date, U.firstname, U.lastname
            FROM Blogs as B, Users as U
            WHERE B.author = U.username AND blogid = %s
        """
        data = (blogid,)
        cursor.execute(query, data)
        blog = cursor.fetchone()

        if blog is None:
            return None

        blog = _join_names(blog)

        # Get tags
        query = "SELECT tag FROM Tags WHERE blogid = %s"
        data = (blogid,)
        cursor.execute(query, data)
        tags = map(lambda tag: tag['tag'], cursor.fetchall())
        blog['tags'] = tags

        # Get comments
        query = """
            SELECT C.commentid as id, C.author, C.sentiment, C.description, C.commentdate as date, U.firstname, U.lastname
            FROM Comments as C, Users as U
            WHERE C.author = U.username AND C.blogid = %s
            ORDER BY C.commentdate DESC, C.commentid DESC
        """
        data = (blogid,)
        cursor.execute(query, data)
        blog['comments'] = map(_join_names, cursor.fetchall())
        return blog
    finally:
        cursor.close()
        db.close()

def q1(username):
    # Get blogs of username where all comments are positive
    db = _connect()
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT blogid as id, author, subject, blogdate as date from Blogs WHERE author = %s and blogid not in (SELECT distinct blogid from Comments WHERE sentiment='negative')"
        data = (username,)
        cursor.execute(query, data)
        return list(cursor.fetchall())
    finally:
        cursor.close()
        db.close()

def q2():
    # Get user(s) who posted the most blogs on 10/10/2020
    db = _connect()
    cursor = db.cursor()
    try:
        query = "SELECT author FROM Blogs GROUP BY author HAVING COUNT(*) = (SELECT MAX(mostcount) FROM (SELECT COUNT(blogid) AS mostcount FROM Blogs GROUP BY author) x)"
        cursor.execute(query)
        return _unwrap_singles(cursor.fetchall())
    finally:
        cursor.close()
        db.close()

def q3(username1, username2):
    # Get users who are followed by both username1 and username2
    db = _connect()
    cursor = db.cursor()
    try:
        query = "SELECT C.leader FROM Follows C, Follows B  WHERE B.leader = C.leader AND C.follower = %s AND B.follower = %s"
        data = (username1,username2,)
        cursor.execute(query, data)
        return _unwrap_singles(cursor.fetchall())
    finally:
        cursor.close()
        db.close()

def q4():
    # Get users who have never posted a blog
    db = _connect()
    cursor = db.cursor()
    try:
        query = "SELECT distinct username FROM Users WHERE username not in (SELECT distinct author from Blogs)"
        cursor.execute(query)
        return _unwrap_singles(cursor.fetchall())
    finally:
        cursor.close()
        db.close()

def q5():
    # Get users who have posted comments and all of them are negative
    db = _connect()
    cursor = db.cursor()
    try:
        query = "SELECT distinct author FROM Comments WHERE sentiment='negative' and author not in (SELECT author from Comments WHERE sentiment='positive')"
        cursor.execute(query)
        return _unwrap_singles(cursor.fetchall())
    finally:
        cursor.close()
        db.close()

def q6():
    # Get users who have never received negative comments on their blogs
    db = _connect()
    cursor = db.cursor()
    try:
        query = "select distinct author from Blogs where author not in (SELECT author FROM Comments WHERE sentiment='negative')"
        cursor.execute(query)
        return _unwrap_singles(cursor.fetchall())
    finally:
        cursor.close()
        db.close()

def _load_sql(file):
    db = _connect()
    with open(file, 'r') as f:
        with db.cursor() as cursor:
            for result in cursor.execute(f.read(), multi=True):
                pass
            db.commit()
            db.close()

def initialize():
    _load_sql('sql/schema.sql')
    _load_sql('sql/triggers.sql')
    _load_sql('sql/data.sql')

def _connect():
    return mysql.connector.connect(
        user='440admin',
        password='password',
        host='127.0.0.1',
        database='440project'
    )
