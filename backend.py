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
    cursor = db.cursor()
    try:
        query = "SELECT blogid,author,subject,blogdate FROM Blogs ORDER BY blogdate DESC,blogid DESC"
        cursor.execute(query)
        result = []
        for (blogid,author,subject,date) in cursor.fetchall():
            result.append({
                'id': blogid,
                'author': author,
                'subject': subject,
                'date': date
            })
        return result
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
            return ErrorCommentsPerDay
        elif err.sqlstate == '99003':
            return ErrorCommentsPerBlog
        elif err.sqlstate == '99004':
            return ErrorCommentOwnBlog
        else:
            raise
    finally:
        cursor.close()
        db.close()

def get_blog(blogid):
    # Returns the given blog along with its tags and comments.
    # If no such blog, return None.
    db = _connect()
    cursor = db.cursor(dictionary=True)
    try:
        # Get blog
        query = "SELECT blogid as id, author, description, blogdate as date FROM Blogs WHERE blogid = %s"
        data = (blogid,)
        cursor.execute(query, data)
        blog = cursor.fetchone()

        if blog is None:
            return None

        # Get tags
        query = "SELECT tag FROM Tags WHERE blogid = %s"
        data = (blogid,)
        cursor.execute(query, data)
        tags = map(lambda tag: tag['tag'], cursor.fetchall())
        blog['tags'] = tags

        # Get comments
        query = "SELECT commentid as id, author, sentiment, description, commentdate as date FROM Comments WHERE blogid=%s"
        data = (blogid,)
        cursor.execute(query, data)
        blog['comments'] = cursor.fetchall()
        return blog
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
