# app_dashboard.py
import streamlit as st
import pandas as pd
from utils.parser import parse_resume
from utils.nlp_processing import clean_text, extract_skills
from utils.scoring import calculate_match_score

st.set_page_config(page_title="Resume Analyzer Dashboard", layout="wide")
st.title("📝 Resume Analyzer Dashboard")

# ---------------------------
# File Upload
# ---------------------------
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
job_desc_file = st.file_uploader("Upload Job Description", type=["txt"])

if resume_file and job_desc_file:
    try:
        # ---------------------------
        # Extract resume text
        # ---------------------------
        if resume_file.type == "text/plain":
            resume_text = resume_file.read().decode("utf-8")
        else:
            resume_data = parse_resume(resume_file)
            if not resume_data or not resume_data.get("raw_text"):
                st.error("Failed to extract text from resume.")
                st.stop()
            resume_text = resume_data.get("raw_text", "")

        # ---------------------------
        # Extract job description text
        # ---------------------------
        job_desc_text = job_desc_file.read().decode("utf-8")

        if not resume_text.strip():
            st.error("No text found in the resume file.")
            st.stop()
        if not job_desc_text.strip():
            st.error("No text found in the job description file.")
            st.stop()

        # ---------------------------
        # Clean text
        # ---------------------------
        resume_clean = clean_text(resume_text)
        jd_clean = clean_text(job_desc_text)

        # ---------------------------
        # Extract skills
        # ---------------------------
        resume_skills = extract_skills(resume_clean)
        jd_skills = extract_skills(jd_clean)

        # ---------------------------
        # Calculate match score
        # ---------------------------
        match_score, matched_skills, missing_skills = calculate_match_score(
            resume_skills=resume_skills,
            jd_skills=jd_skills
        )

        # ---------------------------
        # Display Results
        # ---------------------------
        st.subheader(f"Resume Match Score: {match_score}%")

        # Skills Found
        if resume_skills:
            df_skills = pd.DataFrame({"Skills Found": sorted(resume_skills)})
            st.write("### ✔ Skills Found")
            st.dataframe(df_skills)
        else:
            st.info("No skills detected in the resume.")

        # Missing Skills / Keywords
        if missing_skills:
            df_missing = pd.DataFrame({"Missing Keywords": sorted(missing_skills)})
            st.write("### ❌ Missing Keywords")
            st.dataframe(df_missing)
        else:
            st.success("✅ No missing keywords! Resume matches all job requirements.")

        # Experience Placeholder (future extension)
        st.write("### 📝 Relevant Experience")
        st.info("Experience extraction not implemented yet.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
