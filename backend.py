import mysql.connector

def create_user_table():
    db = _connect()
    _create_user_table(db)
    db.close()

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

def initialize():
    db = _connect()
    with open('sql/initialize.sql', 'r') as f:
        with db.cursor() as cursor:
            for result in cursor.execute(f.read(), multi=True):
                pass
            db.commit()
            db.close()

def _connect():
    return mysql.connector.connect(
        user='440admin',
        password='password',
        host='127.0.0.1',
        database='440project'
    )

def _create_user_table(db):
    cursor = db.cursor()
    query = "CREATE TABLE IF NOT EXISTS users (username VARCHAR(32) PRIMARY KEY, password VARCHAR(32))"
    cursor.execute(query)
    cursor.close()

def _insert_user(db, usernameStr, passwordStr):
    cursor = db.cursor()
    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
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
        query = "SELECT username FROM users WHERE username = %s and password = %s"
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
        query = "SELECT username FROM users WHERE username = %s"
        data = (usernameStr,)
        cursor.execute(query, data)
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(str(err))
    finally:
        cursor.close()
