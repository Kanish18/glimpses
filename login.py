import streamlit as st
from my_utils import auth
from my_utils.auth import authenticate_user

st.set_page_config(page_title="Login", page_icon="🔐")

st.title("Comic Journal - Login")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if authenticate_user(username, password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("Logged in successfully!")
    else:
        st.error("Invalid username or password")

if st.session_state.logged_in:
    st.info("Use the sidebar to go to Character Creation or Journal pages.")