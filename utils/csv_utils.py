import pandas as pd

def save_user_to_csv(csv_path, username, email, hashed_password):
    new_user = pd.DataFrame([[username, email, hashed_password]], columns=['username', 'email', 'password'])
    try:
        df = pd.read_csv(csv_path)
        df = pd.concat([df, new_user], ignore_index=True)
    except FileNotFoundError:
        df = new_user
    df.to_csv(csv_path, index=False)
