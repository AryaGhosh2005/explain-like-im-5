import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Explain Like I'm 5", page_icon="🧸")

st.title("🧸 Explain Like I'm 5")
st.write("Paste any text and get a super simple explanation.")

# Load API key from Streamlit Secrets
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found. Please add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# Configure Gemini
genai.configure(api_key=API_KEY)

# Choose model
model = genai.GenerativeModel("models/gemini-2.5-flash")

def explain_like_five(text):
    prompt = (
        "Explain the following text like you are talking "
        "to a 5-year-old child. Use very simple words, "
        "short sentences, and friendly examples.\n\n"
        + text
    )
    return model.generate_content(prompt).text

# UI
user_text = st.text_area("📄 Paste your text here", height=200)

if st.button("✨ Explain"):
    if user_text.strip() == "":
        st.warning("Please paste some text.")
    elif len(user_text) > 1000:
        st.warning("Please keep text under 1000 characters.")
    else:
        with st.spinner("Explaining in simple words..."):
            explanation = explain_like_five(user_text)
            st.subheader("🌈 Easy Explanation")
            st.write(explanation)

st.caption("⚠️ MVP for educational use only.")
