import streamlit as st
import yaml
from yaml.loader import SafeLoader
import uuid
from pages.home import show_home_page
from pages.admin_db import show_admin_page
#from utils.auth import check_credentials,load_users
from utils.auth_db import check_credentials

def load_config():
    with open('config.yaml') as file:
        return yaml.load(file, Loader=SafeLoader)

# Load the configuration for the authenticator
config = load_config()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

if 'session_id' not in st.session_state:
    st.session_state.session_id = None

if 'show_add_user_form' not in st.session_state:
    st.session_state.show_add_user_form = False

def main():   
    if st.session_state.logged_in:
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.is_admin = False
            st.session_state.session_id = None
            st.experimental_rerun()
        
        if st.session_state.is_admin:
            show_admin_page()
        else:
            show_home_page(st.session_state.username, st.session_state.session_id)
    else:
        login_page()

def login_page():
    with st.form(key='login_form'):
        st.title("Login Page")
        
        st.write("Please enter your credentials to login.")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button(label='Login')
        
        if submit_button:
            #if check_credentials(username, password, config):
            if check_credentials(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.is_admin = username == "admin"  # Example condition to differentiate admin
                st.session_state.session_id = str(uuid.uuid4())
                st.experimental_rerun()
            else:
                st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()
