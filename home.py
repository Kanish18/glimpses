import streamlit as st

st.set_page_config(page_title="📘 Glimpses Home", layout="centered")

# Initialize session state variables if not already present
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("📘 Welcome to Glimpses!")

if st.session_state.logged_in:
    st.success(f"Welcome back, {st.session_state.username}!")
    st.page_link("pages/3_Diary.py", label="Go to Your Diary", icon="📖")
    st.page_link("pages/2_Signup.py", label="Edit Your Avatar", icon="🧙")
else:
    st.warning("You're not logged in.")
    st.page_link("pages/1_Login.py", label="Login", icon="🔐")
    st.page_link("pages/2_Signup.py", label="Sign Up / Create Avatar", icon="🧍‍♂️")
