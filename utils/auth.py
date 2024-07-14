import bcrypt
import pandas as pd
import yaml
from yaml.loader import SafeLoader

def load_config():
    with open('config.yaml') as file:
        return yaml.load(file, Loader=SafeLoader)

def check_credentials(username, password, config):
    credentials = config['credentials']['usernames']

    if username in credentials:
        return bcrypt.checkpw(password.encode(), credentials[username]['password'].encode())
    
    users = load_users('users.csv')
    if username in users:
        print(f"password.encode(){password.encode()}")
        return bcrypt.checkpw(password.encode(),   users[username]['password'].encode())
    
    return False

def add_user(name, email, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    save_user_to_csv('users.csv', name, email, hashed_password)

def load_users(csv_path):
    try:
        df = pd.read_csv(csv_path)
        users = {row['username']: {'email': row['email'], 'password': row['password']} for index, row in df.iterrows()}
        return users
    except FileNotFoundError:
        return {}

def save_user_to_csv(csv_path, username, email, hashed_password):
    print("inside save_user_to_csv")
    new_user = pd.DataFrame([[username, email, hashed_password]], columns=['username', 'email', 'password'])
    try:
        df = pd.read_csv(csv_path)
        df = pd.concat([df, new_user], ignore_index=True)
        print(f"df={df}")
    except FileNotFoundError:
        df = new_user
        print(f"exce df={df}")
    df.to_csv(csv_path, index=False)

def update_user_password(username, new_password):
    users = load_users('users.csv')
    if username in users:
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        users[username]['password'] = hashed_password
        df = pd.DataFrame.from_dict(users, orient='index').reset_index()
        df.columns = ['username', 'email', 'password']
        df.to_csv('users.csv', index=False)
        return True
    return False

def delete_user(username):
    users = load_users('users.csv')
    if username in users:
        users.pop(username)
        df = pd.DataFrame.from_dict(users, orient='index').reset_index()
        df.columns = ['username', 'email', 'password']
        df.to_csv('users.csv', index=False)
        return True
    return False
