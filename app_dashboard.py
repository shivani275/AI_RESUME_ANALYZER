# app_dashboard.py
import streamlit as st
import pandas as pd
from utils.text_extract import extract_text
from utils.nlp_processing import preprocess_text, extract_skills, extract_experience
from utils.scoring import score_resume, suggest_missing_keywords

st.title("Resume Analyzer Dashboard")

# Upload files
resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
job_desc_file = st.file_uploader("Upload Job Description", type=["txt"])

if resume_file and job_desc_file:
    try:
        # ---------------------------
        # Extract text
        # ---------------------------
        resume_text = extract_text(resume_file)
        job_desc_text = extract_text(job_desc_file)

        if not resume_text.strip():
            st.error("No text found in the resume file.")
            st.stop()
        if not job_desc_text.strip():
            st.error("No text found in the job description file.")
            st.stop()

        # ---------------------------
        # Preprocess text
        # ---------------------------
        processed_resume = preprocess_text(resume_text)
        processed_job_desc = preprocess_text(job_desc_text)

        # ---------------------------
        # Extract skills and experience
        # ---------------------------
        resume_skills = extract_skills(processed_resume)
        resume_experience = extract_experience(processed_resume)

        # ---------------------------
        # Score resume
        # ---------------------------
        match_score = score_resume(processed_resume, processed_job_desc)
        missing_keywords = suggest_missing_keywords(resume_skills, processed_job_desc)

        # ---------------------------
        # Display results
        # ---------------------------
        st.subheader(f"Resume Match Score: {match_score}%")

        # Skills Found
        if resume_skills:
            df_skills = pd.DataFrame({"Skills Found": sorted(resume_skills)})
            st.write("### ✔ Skills Found")
            st.dataframe(df_skills)
        else:
            st.info("No skills detected.")

        # Missing Keywords
        if missing_keywords:
            df_missing = pd.DataFrame({"Missing Keywords": sorted(missing_keywords)})
            st.write("### ❌ Missing Keywords")
            st.dataframe(df_missing)
        else:
            st.success("No missing keywords! Resume matches all job requirements.")

        # Relevant Experience
        if resume_experience:
            df_exp = pd.DataFrame({"Relevant Experience": resume_experience})
            st.write("### 📝 Relevant Experience")
            st.dataframe(df_exp)
        else:
            st.info("No experience sections detected.")

    except Exception as e:
        st.error(f"An error occurred: {e}")
