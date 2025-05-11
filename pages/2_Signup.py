import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO
import openai
from supabase import create_client, Client

# --- Setup ---
SUPABASE_URL = "https://mhwepdtjevqupglpurpn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1od2VwZHRqZXZxdXBnbHB1cnBuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njg4NTc0MSwiZXhwIjoyMDYyNDYxNzQxfQ.PiMUgXvBj3gPFbY1j4djF5iE3w9lfOeZQaMu5t1Xce0"  # Keep this secret
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

openai.api_key = "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"
st.set_page_config(page_title="👤 Signup", layout="centered")
st.title("Create Your Comic Avatar")

# Save uploaded image locally
def save_image(uploaded_image):
    folder = "uploaded_avatars"
    os.makedirs(folder, exist_ok=True)
    img_path = os.path.join(folder, uploaded_image.name)
    with open(img_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
    return img_path

# Generate avatar using image + prompt (edit)
def generate_avatar(img_path, prompt):
    try:
        with open(img_path, "rb") as f:
            result = openai.images.edit(
                model="gpt-image-1",
                image=f,
                prompt=prompt,
                size="1024x1024",
                quality="low"
            )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_bytes))

        image = image.resize((300, 300), Image.LANCZOS)
        avatar_path = img_path.replace(".jpg", "_avatar.png").replace(".jpeg", "_avatar.png").replace(".png", "_avatar.png")
        image.save(avatar_path, format="PNG", quality=90)
        return image, avatar_path
    except Exception as e:
        st.error(f"Avatar generation failed: {e}")
        return None, None

# Upload avatar to Supabase Storage
def upload_to_supabase_storage(local_path, user_email):
    try:
        file_name = f"{user_email.replace('@', '_')}_avatar.png"
        with open(local_path, "rb") as f:
            supabase.storage.from_("avatars").upload(file_name, f, {"content-type": "image/png"})

        public_url = f"{SUPABASE_URL}/storage/v1/object/public/avatars/{file_name}"
        return public_url
    except Exception as e:
        st.error(f"Upload to Supabase failed: {e}")
        return None

# Function to create a user and manage password in Supabase Auth
def create_user_with_password(email, password, username):
    try:
        # Create user with email and password using Supabase Auth
        user = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        # After the user is created, insert user details into the "users" table
        user_data = {
            "email": email,
            "username": username,
            "avatar_url": None  # Avatar URL will be added after avatar generation
        }

        # Insert user data into the 'users' table
        supabase.table("users").insert(user_data).execute()
        
        return user
    except Exception as e:
        st.error(f"User creation failed: {e}")
        return None

# Streamlit form
with st.form("signup_form"):
    st.markdown("### 📧 Enter your email")
    user_email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    user_name = st.text_input("Username",placeholder="abc123")

    st.markdown("### 🖼️ Upload your photo")
    uploaded_image = st.file_uploader("Upload an image of yourself", type=["png", "jpg", "jpeg"])

    st.markdown("### ✍️ Describe your avatar style")
    prompt = st.text_input("Example: 'Make me look like a comic superhero standing in a city.'")

    submitted = st.form_submit_button("Generate Avatar")

if submitted:
    if user_email and password and confirm_password and user_name and uploaded_image and prompt.strip():
        if password != confirm_password:
            st.error("Passwords do not match.")
        else:
            with st.spinner("Creating user and generating avatar..."):
                user = create_user_with_password(user_email, password, user_name)
                
                if user:
                    saved_path = save_image(uploaded_image)
                    avatar_image, avatar_path = generate_avatar(saved_path, prompt)

                    if avatar_image:
                        avatar_url = upload_to_supabase_storage(avatar_path, user_email)

                        if avatar_url:
                            # Update user with avatar URL in the 'users' table
                            user_data = {"avatar_url": avatar_url}
                            supabase.table("users").update(user_data).eq("email", user_email).execute()
                            st.success("User created with avatar and profile updated!")

                            st.image(avatar_image, caption="Your Comic Avatar", use_container_width=True)
    else:
        st.warning("Please enter all fields, upload an image, and describe your avatar.")
