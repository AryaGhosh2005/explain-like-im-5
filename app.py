import streamlit as st
import os
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Explain Like I'm 5",
    page_icon="🧸",
    layout="centered"
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🧸 Explain Like I'm 5")
    st.write(
        "Paste any text and get a simple explanation "
        "as if you are explaining it to a 5-year-old."
    )
    st.markdown("---")
    st.markdown("**Built with:**")
    st.markdown("- Streamlit")
    st.markdown("- Python")
    st.markdown("- Gemini AI")
    st.markdown("---")
    st.caption("⚠️ Educational MVP")

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;'>🧸 Explain Like I'm 5</h1>"
    "<p style='text-align:center; color: gray;'>Paste text below and get a simple explanation</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ---------------- API CONFIG ----------------
# Get API key from Streamlit Secrets
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found. Please add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")  # Model that supports generateContent

# ---------------- FUNCTION ----------------
def explain_like_five(text: str) -> str:
    prompt = (
        "Explain the following text like you are talking "
        "to a 5-year-old child. Use very simple words, "
        "short sentences, and friendly examples.\n\n"
        + text
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error("AI failed to generate explanation. Check your API key and quota.")
        return ""

# ---------------- INPUT AREA ----------------
MAX_CHARS = 1000
user_text = st.text_area(
    "📄 Paste your text here",
    height=200,
    placeholder="Example: Newton's First Law states that an object will remain at rest..."
)

char_count = len(user_text)
st.caption(f"Characters: {char_count}/{MAX_CHARS}")

# ---------------- SESSION STATE ----------------
if "explanation" not in st.session_state:
    st.session_state.explanation = ""

# ---------------- BUTTON ----------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    explain_clicked = st.button("✨ Explain Simply", use_container_width=True)

# ---------------- EXPLANATION LOGIC ----------------
if explain_clicked:
    if user_text.strip() == "":
        st.warning("Please paste some text first.")
    elif char_count > MAX_CHARS:
        st.warning("Please keep the text under 1000 characters.")
    else:
        with st.spinner("🧠 Thinking like a friendly teacher..."):
            st.session_state.explanation = explain_like_five(user_text)

# ---------------- DISPLAY RESULT ----------------
if st.session_state.explanation:
    st.markdown("---")
    st.subheader("🌈 Easy Explanation")
    st.markdown(
        f"""
        <div style="
            background-color:#f9f9f9;
            padding:20px;
            border-radius:10px;
            border-left:5px solid #ffcc00;
