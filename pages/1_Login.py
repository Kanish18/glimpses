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
                # Perform login
                auth_response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                # Extract the user from the auth response
                user = auth_response.user

                if user and user.confirmed_at is not None:
                    st.session_state.logged_in = True
                    st.session_state.email = email
                    st.session_state.username = user.user_metadata.get("username", "Guest")
                    st.success("Login successful!")

                    # Redirect to appropriate page
                    if not user.user_metadata.get("username"):
                        st.switch_page("pages/3_Diary.py")
                    else:
                        st.switch_page("pages/2_Signup.py")

                elif user:
                    st.warning("Please confirm your email before logging in.")
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