import streamlit as st

def show_home_page(username,sessionid):
    st.title("Home Page")
    st.write(f"Welcome to the application, {username}!")
    st.write("This is the home page of the application.")

