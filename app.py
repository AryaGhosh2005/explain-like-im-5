import streamlit as st
import os
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Explain / Top Questions",
    page_icon="🧸❓",
    layout="centered"
)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🧸❓ AI Helper")
    st.write(
        "Choose a mode: Explain like a 5-year-old, "
        "or get the top 10 questions about a topic."
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
    "<h1 style='text-align:center;'>🧸❓ AI Helper</h1>"
    "<p style='text-align:center; color: gray;'>Choose a mode and enter text</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ---------------- API CONFIG ----------------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found. Add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")  # works for generateContent

# ---------------- FUNCTIONS ----------------
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
    except Exception:
        return "AI failed to generate explanation. Check your API key and quota."

def generate_top_questions(topic: str) -> str:
    prompt = (
        f"Given the topic or sentence below, generate the top 10 most frequently asked questions about it, "
        f"each question on a new line.\n\nTopic: {topic}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "AI failed to generate questions. Check your API key and quota."

# ---------------- MODE SELECTION ----------------
mode = st.radio("Choose a mode:", ["Explain Like I'm 5", "Top 10 Questions"])

# ---------------- INPUT AREA ----------------
user_text = st.text_area(
    "Enter text or topic:",
    height=200,
    placeholder="Type a sentence or topic here..."
)

# ---------------- SESSION STATE ----------------
if "result" not in st.session_state:
    st.session_state.result = ""

# ---------------- BUTTON ----------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    action_clicked = st.button("🚀 Generate", use_container_width=True)

# ---------------- LOGIC ----------------
if action_clicked:
    if user_text.strip() == "":
        st.warning("Please enter some text first.")
    else:
        with st.spinner("🧠 AI is thinking..."):
            if mode == "Explain Like I'm 5":
                st.session_state.result = explain_like_five(user_text)
            elif mode == "Top 10 Questions":
                st.session_state.result = generate_top_questions(user_text)

# ---------------- DISPLAY RESULT ----------------
if st.session_state.result:
    st.markdown("---")
    if mode == "Explain Like I'm 5":
        st.subheader("🌈 Easy Explanation")
        color = "#ffcc00"
    else:
        st.subheader("🌟 Top 10 Questions")
        color = "#00bfff"

    st.markdown(
        f"""<div style="
            background-color:#f9f9f9;
            padding:20px;
            border-radius:10px;
            border-left:5px solid {color};
            font-size:16px;
        ">
        {st.session_state.result.replace('\n','<br>')}
        </div>""",
        unsafe_allow_html=True
    )
