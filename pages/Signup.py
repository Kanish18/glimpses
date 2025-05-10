# pages/1_Signup.py
import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO
import openai

# --- Configure OpenAI client securely ---
client = openai.OpenAI(api_key="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" )  # Use env variable in production

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
            result = client.images.edit(
                model="gpt-image-1",
                image=f,
                prompt=prompt,
                size="1024x1024",
            )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_bytes))

        # Resize for consistency and save
        image = image.resize((300, 300), Image.LANCZOS)
        avatar_path = img_path.replace(".jpg", "_avatar.jpg").replace(".png", "_avatar.png")
        image.save(avatar_path, format="PNG", quality=90)

        return image, avatar_path
    except Exception as e:
        st.error(f"Avatar generation failed: {e}")
        return None, None

# Streamlit form
with st.form("signup_form"):
    st.markdown("### 🖼️ Upload your photo")
    uploaded_image = st.file_uploader("Upload an image of yourself", type=["png", "jpg", "jpeg"])

    st.markdown("### ✍️ Describe your avatar style")
    prompt = st.text_input("Example: 'Make me look like a comic superhero standing in a city.'")

    submitted = st.form_submit_button("Generate Avatar")

if submitted:
    if uploaded_image and prompt.strip():
        with st.spinner("Generating avatar using AI..."):
            saved_path = save_image(uploaded_image)
            avatar_image, avatar_path = generate_avatar(saved_path, prompt)

            if avatar_image:
                st.image(avatar_image, caption="Your Comic Avatar", use_column_width=True)
                st.success(f"Avatar saved at: `{avatar_path}`")
    else:
        st.warning("Please upload an image and provide a prompt.")
