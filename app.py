# app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from utils.text_extract import extract_text_from_pdf
from utils.nlp_processing import clean_text, extract_keywords, extract_skills
from utils.scoring import calculate_match_score
from utils.database import init_db, save_result, fetch_results
from utils.pdf_report import generate_pdf

# ---------------------------
# Initialize DB
# ---------------------------
init_db()

# ---------------------------
# Predefined Skill List
# ---------------------------
SKILL_LIST = [
    "python", "sql", "excel", "data analysis", "machine learning",
    "communication", "teamwork", "tableau", "power bi", "statistics"
]

def extract_skills_from_jd(jd_text):
    jd_text_lower = jd_text.lower()
    return [skill for skill in SKILL_LIST if skill.lower() in jd_text_lower]

def suggest_resume_improvements(missing_skills):
    return [f"Consider adding '{skill}' to your skills section." for skill in missing_skills]

def validate_resume_for_job(resume_skills, required_skills):
    missing = [skill for skill in required_skills if skill.lower() not in [s.lower() for s in resume_skills]]
    valid = len(missing) == 0
    return valid, missing

# ---------------------------
# Custom CSS for background and buttons
# ---------------------------
st.markdown("""
    <style>
        .reportview-container {
            background: linear-gradient(to right, #f0f4f8, #d9e2ec);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 8px;
            height: 45px;
            width: 100%;
        }
        .stTextArea>div>textarea {
            font-size: 14px;
        }
        .stFileUploader>div>div>label {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar: Past Results
# ---------------------------
st.sidebar.title("📊 Past Analysis")
results = fetch_results(limit=10)
if results:
    for row in results:
        res_id, resume_text, job_desc, score, matched_skills, missing_skills = row
        matched_skills = ", ".join(json.loads(matched_skills)) if matched_skills else ""
        missing_skills = ", ".join(json.loads(missing_skills)) if missing_skills else ""

        if score >= 80:
            color = "#28a745"
        elif score >= 50:
            color = "#ffc107"
        else:
            color = "#dc3545"

        st.sidebar.markdown(
            f"""
            <div style="border:1px solid #ddd; border-radius:8px; padding:8px; margin-bottom:6px;">
                <strong>ID:</strong> {res_id} <br>
                <strong>Score:</strong> 
                <span style="color:white; background-color:{color}; padding:2px 6px; border-radius:4px;">{score}%</span><br>
                <strong>Matched:</strong> {matched_skills if matched_skills else 'None'}<br>
                <strong>Missing:</strong> {missing_skills if missing_skills else 'None'}
            </div>
            """, unsafe_allow_html=True
        )
else:
    st.sidebar.info("No previous results found.")

# ---------------------------
# Main Page
# ---------------------------
st.title("📝 AI Resume Analyzer & Job Match Score")

uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description")

analyze_disabled = not (uploaded_resume and job_description.strip())

if st.button("Analyze", disabled=analyze_disabled):
    with st.spinner("Analyzing resume..."):
        try:
            # Extract resume text
            resume_text = extract_text_from_pdf(uploaded_resume)
            if not resume_text.strip():
                st.error("No text found in the uploaded PDF.")
                st.stop()

            cleaned_resume = clean_text(resume_text)
            cleaned_jd = clean_text(job_description)

            resume_keywords = extract_keywords(cleaned_resume)
            jd_keywords = extract_skills_from_jd(job_description)
            resume_skills = extract_skills(resume_text)

            # Match score calculation
            score, matched, missing = calculate_match_score(resume_skills, jd_keywords)
            score = round(score, 2)

            # Save result in DB
            save_result(
                resume_text=resume_text,
                job_description=job_description,
                score=score,
                matched_skills=matched,
                missing_skills=missing
            )

            # Display match score
            st.subheader(f"Match Score: {score}%")

            # ---------------------------
            # Single Donut Chart for Skill Match
            # ---------------------------
            all_required_skills = set([s.lower() for s in jd_keywords])
            resume_skills_set = set([s.lower() for s in resume_skills])

            matched_set = all_required_skills & resume_skills_set
            missing_set = all_required_skills - resume_skills_set

            if len(all_required_skills) > 0:
                fig_match = go.Figure(go.Pie(
                    labels=["Matched", "Missing"],
                    values=[len(matched_set), len(missing_set)],
                    hole=0.5,
                    marker=dict(colors=["#28a745", "#dc3545"]),
                    textinfo="percent+label",
                    hoverinfo="label+value"
                ))
                fig_match.update_layout(
                    title=f"Skill Match Overview ({len(matched_set)} matched / {len(missing_set)} missing)",
                    showlegend=True,
                    margin=dict(t=50, b=50, l=25, r=25)
                )
                st.plotly_chart(fig_match, use_container_width=True)
            else:
                st.info("No skills found in job description.")

            # ---------------------------
            # Display Missing Keywords Below Chart
            # ---------------------------
            st.markdown("### ❌ Missing Skills / Keywords")
            if missing_set:
                for skill in sorted(missing_set):
                    st.markdown(f"- {skill}")
            else:
                st.success("All required job skills are matched! ✅")

            # ---------------------------
            # Resume validity & improvement suggestions
            # ---------------------------
            valid, missing_required = validate_resume_for_job(resume_skills, jd_keywords)
            st.write("### ✅ Resume Validity for Job")
            if valid:
                st.success("Your resume is VALID for this job! 🎯")
            else:
                st.warning(f"Your resume is MISSING {len(missing_required)} required skills: {', '.join(missing_required)}")

            improvement_suggestions = suggest_resume_improvements(missing_required)
            st.write("### 🛠 Resume Improvement Suggestions")
            if improvement_suggestions:
                for s in improvement_suggestions:
                    st.warning(s)
            else:
                st.success("No improvements needed! Your resume covers all required job skills.")

            # ---------------------------
            # PDF Report Download
            # ---------------------------
            pdf_file_path = generate_pdf(
                candidate_name="Candidate",
                match_score=score,
                skills=matched,
                missing_keywords=missing,
                experience=[],
                file_path="resume_report.pdf"
            )

            with open(pdf_file_path, "rb") as f:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=f,
                    file_name="resume_report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
