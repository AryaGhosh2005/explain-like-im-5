import streamlit as st
import os
import google.generativeai as genai
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Helper",
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
    st.markdown("- PyPDF2")
    st.markdown("---")
    st.caption("⚠️ MVP")

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;'>🧸❓ AI Helper</h1>"
    "<p style='text-align:center; color: gray;'>Paste text, upload PDF, or enter a topic and choose a mode</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ---------------- API CONFIG ----------------
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("API key not found. Add GEMINI_API_KEY in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")  # Supports generateContent

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
    except Exception as e:
        return f"AI failed: {str(e)}"

def generate_top_questions(topic: str) -> str:
    prompt = (
        f"Given the topic or sentence below, generate the top 10 most frequently asked questions about it, "
        f"each question on a new line.\n\nTopic: {topic}"
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI failed: {str(e)}"

# ---------------- MODE SELECTION ----------------
mode = st.radio("Choose a mode:", ["Explain Like I'm 5", "Top 10 Questions"])

# ---------------- INPUT OPTIONS ----------------
input_option = st.radio("Input type:", ["Paste Text", "Upload PDF"])

user_text = ""

if input_option == "Paste Text":
    user_text = st.text_area(
        "Enter text or topic:",
        height=200,
        placeholder="Type a sentence, paragraph, or topic here..."
    )
elif input_option == "Upload PDF":
    uploaded_file = st.file_uploader("📄 Upload a PDF", type=["pdf"])
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        pages_text = []
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
        user_text = "\n".join(pages_text)
        st.text_area("📄 Extracted PDF Text:", user_text, height=200)

char_count = len(user_text)
st.caption(f"Characters: {char_count}")

# ---------------- SESSION STATE ----------------
if "result" not in st.session_state:
    st.session_state.result = ""

# ---------------- BUTTON ----------------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    action_clicked = st.button("🚀 Generate", use_container_width=True)

# ---------------- LOGIC ----------------
if action_clicked:
    if user_text.strip() == "":
        st.warning("Please provide some text or upload a PDF first.")
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
