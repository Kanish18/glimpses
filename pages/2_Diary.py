# pages/4_Diary.py
import streamlit as st
from PIL import Image
st.set_page_config(page_title="📖 Diary Entry", layout="wide")
st.title("Welcome to your Diary")

def diary_page():
    
    st.title("📔 Your Diary")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✍️ Write your story")
        story_input = st.text_area("Memory", height=400, label_visibility="collapsed")
        if st.button("Save Entry"):
            st.success("Story saved! (Note: Add database save logic here.)")

    with col2:
        st.markdown("### 🖼️ Upload an image")
        uploaded_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your Story Image", use_column_width=True)

diary_page()
