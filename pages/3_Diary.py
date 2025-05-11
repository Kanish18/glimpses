# pages/4_Diary.py
import streamlit as st
from PIL import Image
import openai
import requests
from io import BytesIO
import base64
from supabase import create_client,Client

from PIL import Image
from io import BytesIO

# Convert and prepare image
def prepare_image_for_openai(image_path):
    image = Image.open(image_path).convert("RGBA")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# --- Setup ---
SUPABASE_URL = "https://mhwepdtjevqupglpurpn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1od2VwZHRqZXZxdXBnbHB1cnBuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njg4NTc0MSwiZXhwIjoyMDYyNDYxNzQxfQ.PiMUgXvBj3gPFbY1j4djF5iE3w9lfOeZQaMu5t1Xce0"  # Keep this secret
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

openai.api_key = "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"
# Page setup
def generate_ai_image(prompt, avatar_url):
    try:
        # Download avatar
        response = requests.get(avatar_url)
        if response.status_code != 200:
            raise ValueError("Failed to fetch avatar from Supabase.")

        # Convert to PNG buffer
        image = Image.open(BytesIO(response.content)).convert("RGBA")
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.name = "avatar.png"
        buffer.seek(0)

        # Generate image
        result = openai.images.edit(
            model="gpt-image-1",
            image=buffer,
            prompt=prompt,
            size="1024x1024",
            quality="low"
        )

        # Decode result
        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        return Image.open(BytesIO(image_bytes))

    except Exception as e:
        st.error(f"Image generation failed: {e}")
        return None

# --- Main Diary Page ---
def diary_page():
    if "email" not in st.session_state:
        st.warning("You must be logged in to access your diary.")
        return

    if "generated_image" not in st.session_state:
        st.session_state.generated_image = None

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✍️ Write your memory")
        story_input = st.text_area("Memory", height=400, label_visibility="collapsed")

        # Fetch avatar URL
        email = st.session_state.email
        avatar_query = supabase.table("users").select("avatar_url").eq("email", email).single().execute()

        if avatar_query.data:
            avatar_url = avatar_query.data.get("avatar_url")
        else:
            st.error("Avatar not found for this user. Please ensure you have an avatar uploaded.")
            return

        if st.button("Generate AI Image"):
            if story_input.strip() and avatar_url:
                with st.spinner("Generating AI image..."):
                    generated_image = generate_ai_image(story_input, avatar_url)
                    if generated_image:
                        st.session_state.generated_image = generated_image
            else:
                st.warning("Please write something and ensure your avatar is available.")

        if st.button("Save Entry"):
            st.success("Story saved! (Add DB logic here.)")

    with col2:
        st.markdown("### 🖼️ Your AI-Generated Image")
        if st.session_state.generated_image:
            st.image(st.session_state.generated_image, caption="Generated Image", use_container_width=True)

diary_page()