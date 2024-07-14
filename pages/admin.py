# import streamlit as st
# from utils.auth import add_user,load_users,delete_user,update_user_password
# from utils.csv_utils import save_user_to_csv
# import pandas as pd

# def show_admin_page():
#     st.title("Admin Page")
#     if st.button("Add New User"):
#         st.session_state.show_add_user_form = not st.session_state.show_add_user_form

#     if st.session_state.show_add_user_form:
#         st.write("Create a new user:")
        
#         name = st.text_input("Name")
#         email = st.text_input("Email")
#         password = st.text_input("User Password", type="password")
#         confirm_password = st.text_input("Confirm Password", type="password")
    

        
#         if st.button("Create User"):
#             print(f"password:{password},confirm_password:{confirm_password}")
#             if password == confirm_password:
#                 print("step 0")
#                 add_user(name, email, password)
#                 print("step 1")
#                 #save_user_to_csv('users.csv', name, email, password)
#                 print("step 2")
#                 st.success(f"User {name} created successfully!")
#             else:
#                 st.error("Please fill out all fields and ensure passwords match.")
    
#     st.write("Reset User Password:")
#     reset_username = st.text_input("Reset Username")
#     new_password = st.text_input("New Password", type="password")
#     confirm_new_password = st.text_input("Confirm New Password", type="password")
    
#     if st.button("Reset Password"):
#         if new_password and new_password == confirm_new_password:
#             if update_user_password(reset_username, new_password):
#                 st.success(f"Password for {reset_username} has been reset successfully!")
#             else:
#                 st.error(f"User {reset_username} not found.")
#         else:
#             st.error("Please fill out all fields and ensure passwords match.")
    
#     st.write("Delete User:")
#     delete_username = st.text_input("Delete Username")
    
#     if st.button("Delete User"):
#         if delete_user(delete_username):
#             st.success(f"User {delete_username} has been deleted successfully!")
#         else:
#             st.error(f"User {delete_username} not found.")
    
#     st.write("Current Users:")
#     users = load_users('users.csv')
#     if users:
#         df = pd.DataFrame(users).T.reset_index()
#         df.columns = ['Username', 'Email', 'Password']
#         st.table(df.drop(columns=['Password']))
#     else:
#         st.write("No users found.")

import streamlit as st
from utils.auth import add_user, load_users, update_user_password, delete_user
from utils.csv_utils import save_user_to_csv
import pandas as pd

def show_admin_page():
    st.title("Admin Page")

    if "show_add_user_form" not in st.session_state:
        st.session_state.show_add_user_form = False

    if st.button("Add New User"):
        st.session_state.show_add_user_form = not st.session_state.show_add_user_form

    if st.session_state.show_add_user_form:
        st.write("Create a new user:")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Create User"):
            if name and email and password and password == confirm_password:
                add_user(name, email, password)
                save_user_to_csv('users.csv', name, email, password)
                st.success(f"User {name} created successfully!")
                st.session_state.show_add_user_form = False
                st.experimental_rerun()  # Refresh the page to show updated user list
            else:
                st.error("Please fill out all fields and ensure passwords match.")
    
    st.write("Current Users:")
    users = load_users('users.csv')
    
    if users:
        df = pd.DataFrame(users).T.reset_index()
        df.columns = ['Username', 'Email', 'Password']
        
        # Display users in a table
        st.write(df.drop(columns=['Password']))

        # Create a drop-down list for selecting a user
        selected_user = st.selectbox("Select User", df['Username'])
        
        st.write(f"Selected User: {selected_user}")

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Reset Password"):
                new_password = st.text_input("New Password", type="password", key="new_password")
                confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")
                if new_password and new_password == confirm_new_password:
                    if update_user_password(selected_user, new_password):
                        st.success(f"Password for {selected_user} has been reset successfully!")
                    else:
                        st.error(f"User {selected_user} not found.")
                else:
                    st.error("Please fill out all fields and ensure passwords match.")

        with col2:
            if st.button("Delete User"):
                if delete_user(selected_user):
                    st.success(f"User {selected_user} has been deleted successfully!")
                    st.experimental_rerun()  # Refresh the page to show updated user list
                else:
                    st.error(f"User {selected_user} not found.")
    else:
        st.write("No users found.")
