# pages/4_Diary.py
import streamlit as st
from PIL import Image
import openai
import requests
from io import BytesIO
import os

# Set your OpenAI API key
openai.api_key = "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"  # Use your actual key securely in production

st.set_page_config(page_title="📖 Diary Entry", layout="wide")
st.title("Welcome to your Diary")

def generate_ai_image(prompt):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        st.error(f"Failed to generate image: {e}")
        return None

def diary_page():
    st.title("📔 Your Diary")

    if "generated_image_url" not in st.session_state:
        st.session_state.generated_image_url = None

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✍️ Write your story")
        story_input = st.text_area("Memory", height=400, label_visibility="collapsed")

        if st.button("Generate AI Image"):
            if story_input.strip():
                with st.spinner("Generating AI image..."):
                    image_url = generate_ai_image(story_input)
                    if image_url:
                        st.session_state.generated_image_url = image_url
            else:
                st.warning("Please write something in the story box.")

        if st.button("Save Entry"):
            st.success("Story saved! (Note: Add database save logic here.)")

    with col2:
        st.markdown("### 🖼️ Your AI Image")
        if st.session_state.generated_image_url:
            try:
                image_response = requests.get(st.session_state.generated_image_url)
                image = Image.open(BytesIO(image_response.content))
                st.image(image, caption="Generated Image", use_column_width=True)
            except:
                st.error("Failed to load the generated image.")

        uploaded_file = st.file_uploader("Or upload your own image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your Uploaded Image", use_column_width=True)

diary_page()
