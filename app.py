import streamlit as st
import pandas as pd
import numpy as np
import re
from pypdf import PdfReader
from docx import Document
# -------------------------------
# Extract text from PDF
# -------------------------------
def extract_pdf(file):
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
# -------------------------------
# Extract text from DOCX
# -------------------------------
def extract_docx(file):
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
# -------------------------------
# Resume Analyzer Logic
# -------------------------------
def analyze_resume(text):
    skills = ["python", "java", "sql", "machine learning", "html", "css"]
    found_skills = []
    for skill in skills:
        if skill in text.lower():
            found_skills.append(skill)
    score = len(found_skills) * 10
    return found_skills, score
# -------------------------------
# Streamlit UI
# -------------------------------
st.title("📄 Resume Analyzer")
st.write("Upload your resume (PDF or DOCX)")
uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        text = extract_pdf(uploaded_file)
    else:
        text = extract_docx(uploaded_file)
    st.subheader("📃 Extracted Text")
    st.text_area("", text, height=200)
    skills, score = analyze_resume(text)
    st.subheader("✅ Skills Found")
    st.write(skills)
    st.subheader("📊 Resume Score")
    st.success(f"{score} / 100")