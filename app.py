import streamlit as st
import google.generativeai as genai
import os

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
        "This AI tool explains complex text "
        "in very simple words — like teaching a 5-year-old."
    )
    st.markdown("---")
    st.markdown("**Built using:**")
    st.markdown("- Gemini API")
    st.markdown("- Streamlit")
    st.markdown("- Python")
    st.markdown("---")
    st.caption("⚠️ Educational MVP")

# ---------------- MAIN HEADER ----------------
st.markdown(
    """
    <h1 style="text-align:center;">🧸 Explain Like I'm 5</h1>
    <p style="text-align:center; color: gray;">
    Paste any text and get a super simple explanation
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- API KEY ----------------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found. Please add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ---------------- FUNCTION ----------------
def explain_like_five(text):
    prompt = (
        "Explain the following text like you are talking "
        "to a 5-year-old child. Use very simple words, "
        "short sentences, and friendly examples.\n\n"
        + text
    )
    return model.generate_content(prompt).text

# ---------------- INPUT AREA ----------------
MAX_CHARS = 1000

user_text = st.text_area(
    "📄 Paste your text below",
    height=220,
    placeholder="Example: Newton's First Law states that an object will remain at rest..."
)

char_count = len(user_text)
st.caption(f"Characters: {char_count}/{MAX_CHARS}")

# ---------------- BUTTON ----------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    explain_clicked = st.button("✨ Explain Simply", use_container_width=True)

# ---------------- OUTPUT ----------------
if explain_clicked:
    if user_text.strip() == "":
        st.warning("Please paste some text first.")
    elif char_count > MAX_CHARS:
        st.warning("Please keep the text under 1000 characters.")
    else:
        with st.spinner("🧠 Thinking like a friendly teacher..."):
            explanation = explain_like_five(user_text)

        st.markdown("---")
        st.subheader("🌈 Simple Explanation")

        st.markdown(
            f"""
            <div style="
                background-color:#f9f9f9;
                padding:20px;
                border-radius:10px;
                border-left:5px solid #ffcc00;
                font-size:16px;
            ">
            {explanation}
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🚀 MVP built for learning and experimentation")
