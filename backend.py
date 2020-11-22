import mysql.connector

def insert_user(usernameStr, passwordStr):
    db = _connect()
    result = _insert_user(db, usernameStr, passwordStr)
    db.close()
    return result

def verify_user(usernameStr, passwordStr):
    db = _connect()
    result = _verify_user(db, usernameStr, passwordStr)
    db.close()
    return result

def retrieve_user(usernameStr):
    db = _connect()
    result = _retrieve_user(db, usernameStr)
    db.close()
    return result

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

def _insert_user(db, usernameStr, passwordStr):
    cursor = db.cursor()
    try:
        query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
        data = (usernameStr, passwordStr)
        cursor.execute(query, data)
        db.commit()
    except mysql.connector.Error as err:
        print(str(err))
        return False
    finally:
        cursor.close()
                
        print('User is created')

def _verify_user(db, usernameStr, passwordStr):
    cursor = db.cursor()
    try:
        query = "SELECT username FROM Users WHERE username = %s and password = %s"
        data = (usernameStr, passwordStr)
        cursor.execute(query, data)
        result = cursor.fetchone()
        
        if result is None:
            return False
        else:
            return True
    except mysql.connector.Error as err:
        print(str(err))
        return False
    finally:
        cursor.close()
                
def _retrieve_user(db, usernameStr):
    cursor = db.cursor()
    try:
        query = "SELECT username FROM Users WHERE username = %s"
        data = (usernameStr,)
        cursor.execute(query, data)
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(str(err))
    finally:
        cursor.close()

