import streamlit as st
from openai import OpenAI
import os
from fpdf import FPDF
# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Streamlit page config
st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="wide")
st.title("📚 AI Study Buddy")
st.write("Your smart assistant for notes, Q&A, flashcards, quizzes & audio transcription!")

# Sidebar menu
menu = st.sidebar.radio("Choose a feature:", [
    "Ask a Question",
    "Summarize Notes",
    "Generate Flashcards",
    "Quiz Me",
    "Transcribe Audio"
])

# Function: generate response from GPT
def ask_gpt(prompt, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content

# Function: export text to PDF
def save_pdf(text, filename="study_notes.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)
    return filename


# ---------------- Features ---------------- #

# 1. Ask a Question
if menu == "Ask a Question":
    question = st.text_input("Enter your question:")
    if st.button("Get Answer") and question:
        with st.spinner("Thinking..."):
            answer = ask_gpt(f"Answer this question clearly:\n\n{question}")
        st.success(answer)
        if st.button("Save Answer as PDF"):
            filename = save_pdf(answer, "answer.pdf")
            with open(filename, "rb") as f:
                st.download_button("Download PDF", f, file_name="answer.pdf")

# 2. Summarize Notes
elif menu == "Summarize Notes":
    notes = st.text_area("Paste your notes:")
    if st.button("Summarize"):
        with st.spinner("Summarizing..."):
            summary = ask_gpt(f"Summarize these study notes:\n\n{notes}")
        st.info(summary)
        if st.button("Save Summary as PDF"):
            filename = save_pdf(summary, "summary.pdf")
            with open(filename, "rb") as f:
                st.download_button("Download PDF", f, file_name="summary.pdf")

# 3. Generate Flashcards
elif menu == "Generate Flashcards":
    content = st.text_area("Enter topic or notes:")
    if st.button("Create Flashcards"):
        with st.spinner("Generating flashcards..."):
            flashcards = ask_gpt(
                f"Create 5 study flashcards (Q&A format) for:\n\n{content}"
            )
        st.write(flashcards)
        if st.button("Save Flashcards as PDF"):
            filename = save_pdf(flashcards, "flashcards.pdf")
            with open(filename, "rb") as f:
                st.download_button("Download PDF", f, file_name="flashcards.pdf")

# 4. Quiz Me
elif menu == "Quiz Me":
    topic = st.text_input("Enter topic for quiz:")
    if st.button("Start Quiz"):
        with st.spinner("Preparing quiz..."):
            quiz = ask_gpt(f"Create a 5-question quiz with answers on:\n\n{topic}")
        st.write(quiz)
        if st.button("Save Quiz as PDF"):
            filename = save_pdf(quiz, "quiz.pdf")
            with open(filename, "rb") as f:
                st.download_button("Download PDF", f, file_name="quiz.pdf")

# 5. Transcribe Audio
elif menu == "Transcribe Audio":
    uploaded_file = st.file_uploader("Upload audio file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])
    if uploaded_file is not None:
        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                transcript = client.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=uploaded_file
                )
            text = transcript.text
            st.success(text)
            if st.button("Save Transcript as PDF"):
                filename = save_pdf(text, "transcript.pdf")
                with open(filename, "rb") as f:
                    st.download_button("Download PDF", f, file_name="transcript.pdf")
