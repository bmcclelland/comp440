import mysql.connector

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
