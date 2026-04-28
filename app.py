import streamlit as st
import PyPDF2
from groq import Groq

# -----------------------------
# Add your Groq API key here
# -----------------------------
client = Groq(api_key="YOUR_KEY")

st.set_page_config(page_title="AI Resume Analyzer")

st.title("AI Resume Analyzer")
st.write("Upload your resume and get AI feedback.")

# Upload PDF
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job role input
role = st.text_input("Enter Target Job Role")

# Read pdf text
def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


if uploaded_file and role:

    resume_text = extract_text(uploaded_file)

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing..."):

            prompt = f"""
Analyze this resume for the role: {role}

Give:
1. Skills identified
2. Missing skills
3. Resume improvement suggestions
4. Estimated ATS score out of 100
5. 5 interview questions based on the resume

Resume:
{resume_text}
"""

            response = client.chat.completions.create(
                messages=[
                    {
                        "role":"user",
                        "content": prompt
                    }
                ],
                model="llama-3.1-8b-instant"
            )

            result = response.choices[0].message.content

            st.subheader("Analysis Result")
            st.write(result)