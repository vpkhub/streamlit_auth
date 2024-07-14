import psycopg2
from psycopg2 import sql
import hashlib
import yaml
import bcrypt

def load_config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config

DATABASE = load_config()['database']
print(f"DATABASE:{DATABASE}")

def connect_db():
    conn = psycopg2.connect(**DATABASE)
    return conn

def add_user(username, email, password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute(
        sql.SQL("INSERT INTO dbo.users (username, email, password) VALUES (%s, %s, %s)"),
        [username, email, hashed_password]
    )
    conn.commit()
    cursor.close()
    conn.close()

def load_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT username, email, password FROM dbo.users u where u.username !='admin' "))
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return {user[0]: {'email': user[1], 'password': user[2]} for user in users}

def update_user_password(username, new_password):
    conn = connect_db()
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    cursor.execute(
        sql.SQL("UPDATE dbo.users SET password = %s WHERE username = %s"),
        [hashed_password, username]
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True

def delete_user(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("DELETE FROM dbo.users WHERE username = %s"),
        [username]
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True

def check_credentials(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        sql.SQL("SELECT password FROM dbo.users WHERE username = %s"),
        [username]
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        stored_password = result[0]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == stored_password
    return False