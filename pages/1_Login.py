# pages/1_Login.py
import streamlit as st
from supabase import create_client, Client

# --- Setup ---
SUPABASE_URL = "https://mhwepdtjevqupglpurpn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1od2VwZHRqZXZxdXBnbHB1cnBuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njg4NTc0MSwiZXhwIjoyMDYyNDYxNzQxfQ.PiMUgXvBj3gPFbY1j4djF5iE3w9lfOeZQaMu5t1Xce0"  # Keep this secret
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def login():
    st.title("🔐 Login")

    # Check if the user is logged in (Session state)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.success("You are already logged in!")
        st.button("Go to Character Creation", on_click=lambda: st.session_state.update({"page": "2_CreateCharacter.py"}))
        return  # Stop further code execution as user is logged in

    # If the user is not logged in, show the login form
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            try:
                # Attempt to sign in with Supabase Auth
                user = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                # Check if the email is confirmed
                if user and user.user_metadata.get("email_confirmed") == True:
                    st.session_state.logged_in = True
                    st.session_state.email = email
                    st.session_state.username = user.user_metadata.get("username", "Guest")
                    st.success("Login successful!")

                    # Redirect to Diary page or Character Creation based on conditions
                    if not user.user_metadata.get("username"):  # If username is missing, redirect to signup
                        st.session_state.page = "2_CreateCharacter.py"
                        st.experimental_rerun()
                    else:
                        st.session_state.page = "2_Diary.py"
                        st.experimental_rerun()

                elif user:
                    st.warning("Please confirm your email before logging in. Check your inbox for the confirmation email.")
                else:
                    st.error("Invalid email or password.")
            except Exception as e:
                st.error(f"Login failed: {e}")
        else:
            st.warning("Please enter both email and password.")

    # Add a link to the signup page
        st.page_link("pages/2_Signup.py", label="Don't have an account? Sign Up Here")


# Call the login function
login()