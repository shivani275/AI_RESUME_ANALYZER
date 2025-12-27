# app.py
import streamlit as st
import json
import plotly.express as px
from typing import List
from utils.analyzer import analyze_resume
from utils.database import init_db, fetch_results
from utils.pdf_report import generate_pdf
from utils.jd_library import JD_LIBRARY
from utils.nlp_processing import extract_skills
from utils.parser import parse_resume


# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.markdown("""
<style>

/* =========================
GLOBAL VARIABLES
========================= */
:root {
    --bg-main: #0b0f19;
    --bg-card: #111827;
    --bg-soft: #0f172a;
    --border-soft: #1f2937;
    --text-main: #e5e7eb;
    --text-muted: #9ca3af;
    --accent: #8b5cf6;
    --accent-soft: #ede9fe;
    --success: #22c55e;
    --danger: #ef4444;
}

/* =========================
APP BACKGROUND
========================= */
.stApp {
    background: radial-gradient(circle at top left, #1e293b, #020617);
    color: var(--text-main);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* =========================
HERO HEADER
========================= */
.hero {
    width: 100%;
    max-width: 950px;
    margin: 2rem auto 3rem auto;
    padding: 2.5rem 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg, #4f46e5, #0f172a);
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    text-align: center;
}

.hero-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 999px;
    background: rgba(255,255,255,0.15);
    color: #ede9fe;
    font-weight: 700;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    margin-bottom: 14px;
}

.hero-title {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
}

.hero-subtitle {
    font-size: clamp(1rem, 2.5vw, 1.2rem);
    color: #c7d2fe;
    line-height: 1.6;
}

/* =========================
MAIN CONTENT CARD
========================= */
.block-container {
    background: rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(18px);
    border-radius: 24px;
    padding: 2.4rem 2.8rem;
    border: 1px solid #1e2937;
    box-shadow: 0 50px 100px rgba(0,0,0,0.55);
    max-width: 950px;
    margin: auto;
}

/* =========================
SECTION CARD (OPTIONAL WRAPPER)
========================= */
.section-card {
    background: linear-gradient(145deg, #111827, #0f172a);
    border-radius: 20px;
    padding: 20px 24px;
    margin: 24px 0;
    border: 1px solid #1e2937;
    box-shadow: 0 20px 40px rgba(0,0,0,0.35);
}

/* =========================
SECTION TITLES
========================= */
h2 {
    font-size: 1.45rem;
    font-weight: 700;
    color: #f9fafb;
    margin-top: 2.2rem;
    margin-bottom: 1rem;
}

/* =========================
RADIO OPTIONS (CARD STYLE)
========================= */
div[role="radiogroup"] {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 14px;
    margin-top: 12px;
}

div[role="radiogroup"] label {
    background: linear-gradient(145deg, #020617, #020617);
    border-radius: 18px;
    padding: 14px 18px;
    border: 1px solid #1e2937;
    color: #e5e7eb;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
}

div[role="radiogroup"] label:hover {
    border-color: #8b5cf6;
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(139,92,246,0.35);
}

/* =========================
SELECT / TEXTAREA
========================= */
select, textarea {
    background: linear-gradient(145deg, #020617, #020617) !important;
    border-radius: 16px !important;
    border: 1px solid #1e2937 !important;
    color: #f9fafb !important;
    padding: 14px !important;
    font-size: 0.95rem !important;
}

select:focus, textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.4);
}

/* =========================
FILE UPLOADER
========================= */
[data-testid="stFileUploader"] {
    background: linear-gradient(145deg, #020617, #020617);
    border-radius: 22px;
    border: 2px dashed #6366f1;
    padding: 26px;
    text-align: center;
    transition: all 0.25s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #8b5cf6;
    box-shadow: 0 20px 40px rgba(139,92,246,0.25);
}

/* =========================
BUTTONS
========================= */
button[kind="primary"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 18px;
    padding: 12px 36px;
    font-weight: 700;
    letter-spacing: 0.03em;
    border: none;
    transition: all 0.25s ease;
}

button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 20px 45px rgba(139,92,246,0.45);
}

/* =========================
SKILL PILLS
========================= */
.skill-pill {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 0.85rem;
    margin: 8px 8px 0 0;
    background: linear-gradient(145deg, #1e293b, #020617);
    color: #c7d2fe;
    border: 1px solid #312e81;
}

.skill-pill.missing {
    background: linear-gradient(145deg, #1f2937, #020617);
    color: #fecaca;
    border: 1px solid #7f1d1d;
}

/* =========================
SCORE CARD
========================= */
.score-card {
    background: linear-gradient(145deg, #020617, #020617);
    border: 1px solid #1e2937;
    padding: 32px;
    border-radius: 22px;
    text-align: center;
    margin: 36px 0;
}

.score-card h1 {
    font-size: 3.6rem;
    font-weight: 800;
    color: #8b5cf6;
}

/* =========================
ALERTS
========================= */
.stAlert {
    border-radius: 18px;
    border: 1px solid #1e2937;
}

/* =========================
PLOTLY
========================= */
.js-plotly-plot {
    background: transparent !important;
}

/* =========================
SIDEBAR
========================= */
[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1e2937;
}

/* =========================
MOBILE
========================= */
@media (max-width: 768px) {
    .block-container {
        padding: 1.6rem;
        border-radius: 18px;
    }

    div[role="radiogroup"] {
        grid-template-columns: 1fr;
    }

    .score-card h1 {
        font-size: 2.6rem;
    }
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Hero Header HTML
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-POWERED ATS ANALYSIS</div>
    <div class="hero-title">Resume Intelligence Platform</div>
    <div class="hero-subtitle">
        Instantly analyze resumes, identify ATS gaps, 
        visualize skill alignment, and receive rewrite recommendations
        tailored to your target role.
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Initialize
# --------------------------------------------------
init_db()
st.session_state.setdefault("parsed_resume", None)
st.session_state.setdefault("result", None)


# --------------------------------------------------
# Sidebar – Past Analysis
# --------------------------------------------------
with st.sidebar.expander("📊 Past Analysis"):
    rows = fetch_results(limit=10)
    if not rows:
        st.info("No past results.")
    else:
        for r in rows:
            _, _, _, score, matched_json, missing_json, _ = r
            matched = json.loads(matched_json or "[]")
            missing = json.loads(missing_json or "[]")
            badge = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
            st.markdown(f"""
**{badge} {score}%**  
Matched: {", ".join(matched) or "None"}  
Missing: {", ".join(missing) or "None"}  
---
""")

# --------------------------------------------------
# Resume Upload
# --------------------------------------------------
st.markdown("## 📂 Upload Resume")
uploaded_resume = st.file_uploader(
    "PDF or DOCX only",
    type=["pdf", "docx"]
)

if uploaded_resume is not None:
    with st.spinner("Parsing resume..."):
        try:
            parsed = parse_resume(uploaded_resume)
        except Exception as e:
            parsed = None

    if parsed and parsed.get("raw_text"):
        st.session_state["parsed_resume"] = parsed

        st.success("✅ Resume parsed successfully")

        # Safe preview (responsive + capped length)
        preview_text = parsed["raw_text"][:400]
        if len(parsed["raw_text"]) > 400:
            preview_text += "..."

        st.markdown(
            f"""
            <div style="
                background:#f1f5f9;
                padding:1rem;
                border-radius:10px;
                font-size:0.9rem;
                line-height:1.6;
                color:#0f172a;
            ">
            {preview_text}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.session_state["parsed_resume"] = None

        st.error(
            "❌ **Resume parsing failed**\n\n"
            "Possible reasons:\n"
            "- Scanned (image-only) PDF\n"
            "- Protected or corrupted file\n"
            "- Unsupported formatting\n\n"
            "✅ **Tip:** Upload a text-based PDF or DOCX file."
        )



# --------------------------------------------------
# Job Description Mode
# --------------------------------------------------
st.markdown("## 🎯 Job Description")

jd_mode = st.radio(
    "Select Mode",
    ["📋 Predefined Role", "🌐 Universal Check", "✍️ Custom JD"],
    horizontal=True
)

job_description = ""

if jd_mode == "📋 Predefined Role":
    role = st.selectbox("Choose Role", list(JD_LIBRARY.keys()))
    job_description = JD_LIBRARY.get(role, "")

elif jd_mode == "🌐 Universal Check":
    job_description = JD_LIBRARY.get("Universal Resume Check", "")

else:
    job_description = st.text_area("Paste Job Description", height=220)

st.text_area(
    "Active Job Description",
    job_description,
    height=160,
    disabled=True
)


# --------------------------------------------------
# Skill Heatmap Function
# --------------------------------------------------
def plot_skill_heatmap(matched: List[str], missing: List[str]):
    matched = matched or []
    missing = missing or []

    all_skills = list(dict.fromkeys(matched + missing))
    if not all_skills:
        return None

    values = [1 if skill in matched else 0 for skill in all_skills]

    fig = px.bar(
        x=all_skills,
        y=values,
        color=values,
        color_discrete_map={1: "#22c55e", 0: "#ef4444"},
        text=["✔ Matched" if v else "❌ Missing" for v in values],
        title="🎯 Skill Match Heatmap"
    )

    fig.update_layout(
        height=320,
        yaxis=dict(showticklabels=False),
        xaxis_title="Skills",
        margin=dict(l=10, r=10, t=60, b=40),
        showlegend=False
    )

    return fig


# --------------------------------------------------
# Analyze Button
# --------------------------------------------------
analyze_disabled = not uploaded_resume or not job_description.strip()

if st.button("🔍 Analyze Resume", disabled=analyze_disabled):
    with st.spinner("Running ATS analysis..."):
        try:
            st.session_state.result = analyze_resume(
                resume_file=uploaded_resume,
                job_description=job_description
            )
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")


# --------------------------------------------------
# Results Section
# --------------------------------------------------
result = st.session_state.get("result")

if result:
    # ---------------------------
    # Score Card
    # ---------------------------
    st.markdown(
        f"""
        <div class="score-card">
            <h1>{result.get("match_score", 0)}%</h1>
            <p>ATS Match Score</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------
    # Matched Skills
    # ---------------------------
    st.markdown("## ✅ Matched Skills")

    matched_skills = result.get("matched_skills", [])
    if matched_skills:
        for skill in matched_skills:
            st.markdown(
                f"<span class='skill-pill'>{skill}</span>",
                unsafe_allow_html=True
            )
    else:
        st.info("No matched skills found.")

    # ---------------------------
    # Missing Skills
    # ---------------------------
    missing_skills = result.get("missing_skills", [])

    if missing_skills:
        st.markdown("## ❌ Missing Skills (ATS Gaps)")
        for skill in missing_skills:
            st.markdown(
                f"<span class='skill-pill missing'>{skill}</span>",
                unsafe_allow_html=True
            )

    # ---------------------------
    # ATS Feedback
    # ---------------------------
    feedback = result.get("feedback", [])

    if feedback:
        st.markdown("## 🛠 ATS Feedback")
        for msg in feedback:
            st.warning(msg)

    # ---------------------------
    # Skill Heatmap (RESTORED)
    # ---------------------------
    heatmap_fig = plot_skill_heatmap(matched_skills, missing_skills)
    if heatmap_fig:
        st.markdown("## 📊 Skill Match Visualization")
        st.plotly_chart(heatmap_fig, use_container_width=True)

    # ---------------------------
    # Rewrite Suggestions
    # ---------------------------
    rewrite_suggestions = result.get("rewrite_suggestions", [])

    if rewrite_suggestions:
        st.markdown("## ✍️ Resume Rewrite Suggestions")
        for suggestion in rewrite_suggestions:
            st.markdown(
                f"**{suggestion.get('skill')}** "
                f"({suggestion.get('recommended_section', 'Experience / Projects')})"
            )
            st.markdown(f"- {suggestion.get('suggested_rewrite', '')}")

    # ---------------------------
    # PDF Export
    # ---------------------------
    try:
        pdf_path = generate_pdf(
            candidate_name=result.get("candidate", "Candidate"),
            match_score=result.get("match_score", 0),
            skills=matched_skills,
            missing_keywords=missing_skills,
            experience=list(result.get("sections", {}).keys()),
            file_path="resume_report.pdf"
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download ATS Report",
                f,
                file_name="resume_report.pdf"
            )

    except Exception as e:
        st.error(f"❌ PDF generation failed: {e}")
