import streamlit as st
import openai
import requests
import base64
from PIL import Image
from io import BytesIO
from supabase import create_client, Client
import streamlit.components.v1 as components

# --- Setup ---
SUPABASE_URL = "https://mhwepdtjevqupglpurpn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1od2VwZHRqZXZxdXBnbHB1cnBuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0Njg4NTc0MSwiZXhwIjoyMDYyNDYxNzQxfQ.PiMUgXvBj3gPFbY1j4djF5iE3w9lfOeZQaMu5t1Xce0"  # Keep this secret
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

openai.api_key = "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"

# --- Helper fetch avatar and prepare buffer ---
def get_avatar_buffer(email):
    avatar_query = supabase.table("users").select("avatar_url").eq("email", email).single().execute()
    if not avatar_query.data or "avatar_url" not in avatar_query.data:
        raise ValueError("Avatar not found for user.")
    
    avatar_url = avatar_query.data["avatar_url"]
    response = requests.get(avatar_url)
    if response.status_code != 200:
        raise ValueError("Failed to download avatar image.")

    image = Image.open(BytesIO(response.content)).convert("RGBA")
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.name = "avatar.png"  # Required for OpenAI
    buffer.seek(0)
    return buffer

# --- Helper: edit image with gpt-image-1 ---
def edit_avatar_with_prompt(avatar_buffer, prompt):
    try:
        result = openai.images.edit(
            model="gpt-image-1",
            image=avatar_buffer,
            prompt=prompt,
            size="1024x1024",
            quality="low"
        )
        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        return Image.open(BytesIO(image_bytes))
    except Exception as e:
        st.error(f"Failed to generate image for prompt '{prompt}': {e}")
        return None

# --- Vision Board Page ---
def vision_board_page():
    st.title("🌈 Your Vision Board")

    if "email" not in st.session_state:
        st.warning("You must be logged in to access this page.")
        return

    prompts = []
    for i in range(4):
        prompt = st.text_input(f"Dream {i+1}", key=f"vb_prompt_{i}")
        prompts.append(prompt)

    if st.button("Generate Vision Board"):
        try:
            avatar_buffer = get_avatar_buffer(st.session_state.email)
        except Exception as e:
            st.error(str(e))
            return

        generated_images = []
        with st.spinner("Generating your vision board..."):
            for prompt in prompts:
                if prompt.strip():
                    avatar_buffer.seek(0)  # rewind for each prompt
                    img = edit_avatar_with_prompt(avatar_buffer, prompt)
                    if img:
                        buffered = BytesIO()
                        img.save(buffered, format="PNG")
                        base64_img = base64.b64encode(buffered.getvalue()).decode()
                        generated_images.append(base64_img)

        if generated_images:
            st.success("Vision board created!")

            # Render carousel
            slides = "".join([
                f'<div><img src="data:image/png;base64,{img}" style="width:100%; border-radius:10px;"/></div>'
                for img in generated_images
            ])

            carousel_html = f"""
            <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.css"/>
            <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick-theme.min.css"/>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/slick-carousel/1.8.1/slick.min.js"></script>

            <div class="slider">{slides}</div>

            <script>
            $(document).ready(function(){{
                $('.slider').slick({{
                    dots: true,
                    infinite: true,
                    speed: 500,
                    slidesToShow: 1,
                    adaptiveHeight: true
                }});
            }});
            </script>

            <style>
            .slick-slide img {{
                margin: auto;
                display: block;
            }}
            </style>
            """
            components.html(carousel_html, height=600)

vision_board_page()
