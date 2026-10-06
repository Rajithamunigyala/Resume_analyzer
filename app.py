import streamlit as st
from pypdf import PdfReader
from docx import Document


# ---------------- PDF TEXT EXTRACTION ----------------
def extract_pdf(file):
    text = ""
    reader = PdfReader(file)

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# ---------------- DOCX TEXT EXTRACTION ----------------
def extract_docx(file):
    doc = Document(file)
    return "\n".join(para.text for para in doc.paragraphs)


# ---------------- RESUME SKILLS ----------------
def analyze_resume(text):
    all_skills = [
        "python",
        "java",
        "sql",
        "machine learning",
        "html",
        "css",
        "django",
        "flask",
        "javascript",
        "react"
    ]

    found_skills = []

    for skill in all_skills:
        if skill in text.lower():
            found_skills.append(skill)

    score = int(
        (len(found_skills) / len(all_skills)) * 100
    )

    return found_skills, score


# ---------------- MISSING SKILLS ----------------
def missing_skills(found_skills):
    all_skills = [
        "python",
        "java",
        "sql",
        "machine learning",
        "html",
        "css",
        "django",
        "flask",
        "javascript",
        "react"
    ]

    return [
        skill
        for skill in all_skills
        if skill not in found_skills
    ]


# ---------------- ATS SCORE ----------------
def calculate_ats_score(text):
    text = text.lower()

    score = 0

    sections = [
        "education",
        "skills",
        "projects",
        "experience",
        "certifications"
    ]

    for section in sections:
        if section in text:
            score += 10

    keywords = [
        "python",
        "java",
        "sql",
        "machine learning",
        "internship"
    ]

    for keyword in keywords:
        if keyword in text:
            score += 10

    return min(score, 100)


# ---------------- JOB DESCRIPTION MATCH ----------------
def job_match(resume_text, job_description):

    skills = [
        "python",
        "java",
        "sql",
        "machine learning",
        "html",
        "css",
        "django",
        "flask",
        "javascript",
        "react"
    ]

    resume = resume_text.lower()
    job = job_description.lower()

    job_skills = []
    matching_skills = []
    missing_job_skills = []

    for skill in skills:

        if skill in job:

            job_skills.append(skill)

            if skill in resume:
                matching_skills.append(skill)
            else:
                missing_job_skills.append(skill)

    if len(job_skills) > 0:

        match_score = int(
            (len(matching_skills) / len(job_skills)) * 100
        )

    else:
        match_score = 0

    return (
        match_score,
        matching_skills,
        missing_job_skills
    )


# ================= MAIN APP =================

st.title("📄 Resume Analyzer")

st.write(
    "Upload your resume to analyze skills, ATS score "
    "and job matching."
)


# ---------------- UPLOAD ----------------

uploaded_file = st.file_uploader(
    "📤 Upload Resume",
    type=["pdf", "docx"]
)


if uploaded_file is not None:

    # Extract text

    if uploaded_file.type == "application/pdf":

        text = extract_pdf(uploaded_file)

    else:

        text = extract_docx(uploaded_file)


    # ---------------- EXTRACTED TEXT ----------------

    st.subheader("📃 Extracted Resume Text")

    st.text_area(
        "Resume Text",
        text,
        height=200
    )


    # ---------------- SKILLS ----------------

    skills, resume_score = analyze_resume(text)

    st.subheader("✅ Skills Found")

    if skills:

        st.write(skills)

    else:

        st.write("No skills found")


    # ---------------- MISSING SKILLS ----------------

    missing = missing_skills(skills)

    st.subheader("❌ Missing Skills")

    if missing:

        st.write(missing)

    else:

        st.success(
            "No missing skills 🎉"
        )


    # ---------------- RESUME SCORE ----------------

    st.subheader("📊 Resume Score")

    st.progress(resume_score)

    st.success(
        f"Resume Score: {resume_score} / 100"
    )


    # ---------------- ATS SCORE ----------------

    ats_score = calculate_ats_score(text)

    st.subheader("🤖 ATS Score")

    st.progress(ats_score)

    if ats_score >= 80:

        st.success(
            f"Excellent ATS Score: {ats_score} / 100 🎉"
        )

    elif ats_score >= 60:

        st.warning(
            f"Good ATS Score: {ats_score} / 100 👍"
        )

    else:

        st.error(
            f"Low ATS Score: {ats_score} / 100 ⚠️"
        )


    # ---------------- ATS SUGGESTIONS ----------------

    st.subheader("💡 ATS Suggestions")

    text_lower = text.lower()

    suggestions = []

    if "education" not in text_lower:

        suggestions.append(
            "Add an Education section"
        )

    if "skills" not in text_lower:

        suggestions.append(
            "Add a Skills section"
        )

    if "projects" not in text_lower:

        suggestions.append(
            "Add a Projects section"
        )

    if "experience" not in text_lower:

        suggestions.append(
            "Add an Experience section"
        )

    if "certifications" not in text_lower:

        suggestions.append(
            "Add Certifications if available"
        )


    if suggestions:

        for suggestion in suggestions:

            st.write(
                "⚠️",
                suggestion
            )

    else:

        st.success(
            "All important resume sections are present ✅"
        )


    # ================= JOB MATCHING =================

    st.subheader("💼 Job Description Matching")

    st.write(
        "Paste the job description below "
        "to check how well your resume matches."
    )


    job_description = st.text_area(
        "📋 Paste Job Description",
        height=200
    )


    if st.button("🔍 Check Job Match"):

        if job_description.strip() == "":

            st.warning(
                "Please paste a job description."
            )

        else:

            (
                match_score,
                matching,
                missing_job
            ) = job_match(
                text,
                job_description
            )


            # ---------------- MATCH SCORE ----------------

            st.subheader("🎯 Job Match Score")

            st.progress(match_score)

            if match_score >= 80:

                st.success(
                    f"Excellent Match: {match_score}% 🎉"
                )

            elif match_score >= 60:

                st.warning(
                    f"Good Match: {match_score}% 👍"
                )

            else:

                st.error(
                    f"Low Match: {match_score}% ⚠️"
                )


            # ---------------- MATCHING SKILLS ----------------

            st.subheader("✅ Matching Skills")

            if matching:

                st.write(matching)

            else:

                st.write(
                    "No matching skills found"
                )


            # ---------------- MISSING JOB SKILLS ----------------

            st.subheader("❌ Missing Job Skills")

            if missing_job:

                st.write(missing_job)

            else:

                st.success(
                    "No important job skills are missing 🎉"
                )