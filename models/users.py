import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
from flask_mysqldb import MySQL
import bcrypt

def verify_user(username, password, mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account and bcrypt.checkpw(password.encode(), account['password'].encode()):
            return account
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
    return None

def verify_user_already_exists(username, email,mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    print(email)
    try:
        cursor.execute('SELECT * FROM accounts WHERE username = %s OR email = %s', (username, email,))
        account = cursor.fetchone()
        if account:
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
    return False


def create_user(username, password,email,mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), email))
        mysql.connection.commit()
        print("User created successfully")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
    return False

def user_info(id,mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id,))
        accounts = cursor.fetchone()
        return accounts
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
    return None

def update_user(id,username,email,mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute('UPDATE accounts SET username = %s, email = %s WHERE id = %s', (username, email, id))
        mysql.connection.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
    return None

def update_password(id,new_password,mysql):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        print("ACA ESTOY",new_password)
        cursor.execute('UPDATE accounts SET password = %s WHERE id = %s', (bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode(), id))
        mysql.connection.commit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
    return None
