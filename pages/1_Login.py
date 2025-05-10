# pages/1_Login.py
import streamlit as st
#from utils.auth import verify_login
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from my_utils import auth

def login():
    st.title("🔐 Login")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.success("You are already logged in!")
        st.page_link("pages/2_CreateCharacter.py", label="Go to Character Creation")
        return

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.verify_login(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            #st.rerun()
            st.switch_page("pages/2_Diary.py")
        else:
            st.error("Invalid username or password.")

login()
