"""
analyzer.py
------------
Central module for ATS-style resume analysis.
Rule-based, stable, recruiter-accurate.
"""

from typing import Dict, Any, List
import logging

from .parser import parse_resume
from .nlp_processing import clean_text, extract_skills
from .scoring import calculate_match_score, calculate_resume_strength
from .validator import validate_resume_sections
from .database import save_result
from .llm_rewriter import llm_rewrite_skills
from .rewrite_templates import generate_rewrite_suggestions
from .skill_gap import generate_skill_gap_roadmap

# --------------------------------------------------
# ATS Skill Buckets (Recruiter-style)
# --------------------------------------------------
CORE_SKILLS = {
    "python", "java", "javascript", "sql",
    "data structures", "algorithms",
    "oop", "git", "rest api"
}

SECONDARY_SKILLS = {
    "flask", "django", "streamlit",
    "machine learning", "nlp",
    "pandas", "numpy", "docker",
    "aws", "ci/cd", "react"
}


# --------------------------------------------------
# Resume Bullet Generator (Safe fallback)
# --------------------------------------------------
def generate_resume_bullet(skill: str, job_description: str) -> str:
    templates = [
        "Developed and implemented {skill}-based solutions aligned with business requirements.",
        "Applied {skill} to improve system performance and reliability.",
        "Worked hands-on with {skill} in real-world academic and personal projects.",
        "Utilized {skill} to design scalable and maintainable application features."
    ]
    return templates[hash(skill) % len(templates)].format(skill=skill)


# --------------------------------------------------
# Main ATS Resume Analyzer
# --------------------------------------------------
def analyze_resume(
    resume_file,
    job_description: str,
    candidate_name: str = "Candidate"
) -> Dict[str, Any]:

    result: Dict[str, Any] = {}

    # ---------------------------
    # 1. Parse Resume
    # ---------------------------
    resume_data = parse_resume(resume_file)
    if not resume_data or not resume_data.get("raw_text"):
        raise ValueError("Resume parsing failed or empty.")

    resume_text = resume_data["raw_text"]

    if not job_description or not job_description.strip():
        raise ValueError("Invalid job description.")

    # ---------------------------
    # 2. Clean Text
    # ---------------------------
    resume_text_clean = clean_text(resume_text)
    jd_text_clean = clean_text(job_description)

    # ---------------------------
    # 3. Extract Skills
    # ---------------------------
    resume_skills = sorted(set(extract_skills(resume_text_clean)))
    jd_skills = sorted(set(extract_skills(jd_text_clean)))

    # ---------------------------
    # 4. ATS Skill Match Score
    # ---------------------------
    ats_score, matched_skills, missing_skills = calculate_match_score(
        resume_skills=resume_skills,
        jd_skills=jd_skills
    )

    # ---------------------------
    # 5. Core Skill Risk Analysis
    # ---------------------------
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    core_required = jd_set & CORE_SKILLS
    core_missing = sorted(core_required - resume_set)

    # ---------------------------
    # 6. Resume Strength
    # ---------------------------
    resume_strength = calculate_resume_strength(
        resume_text=resume_text_clean,
        resume_skills=resume_skills
    )

    # ---------------------------
    # 7. Section Validation
    # ---------------------------
    sections_status = validate_resume_sections(resume_text_clean)

    # ---------------------------
    # 8. ATS Feedback
    # ---------------------------
    feedback: List[str] = []

    if core_missing:
        feedback.append(
            f"❌ Critical ATS Risk: Missing core skills ({', '.join(core_missing)})."
        )

    if ats_score < 60:
        feedback.append(
            "⚠️ Low ATS compatibility. Resume may be auto-rejected."
        )

    if resume_strength < 70:
        feedback.append(
            "📝 Resume quality is weak. Improve formatting and add measurable achievements."
        )

    missing_sections = [
        s for s, present in sections_status.items() if not present
    ]
    if missing_sections:
        feedback.append(
            f"📄 Missing resume sections: {', '.join(missing_sections)}."
        )

    # ---------------------------
    # 9. Skill Gap Roadmap
    # ---------------------------
    skill_gap_roadmap = generate_skill_gap_roadmap(
        jd_skills=jd_skills,
        resume_skills=resume_skills
    )

    # ---------------------------
    # 10. Rewrite Suggestions
    # ---------------------------
    try:
        rewrite_suggestions = llm_rewrite_skills(
            skills=missing_skills,
            job_description=job_description
        )
    except Exception:
        rewrite_suggestions = generate_rewrite_suggestions(missing_skills)

    # ---------------------------
    # 11. Final Result
    # ---------------------------
    result.update({
        "candidate": candidate_name,
        "match_score": ats_score,
        "resume_strength": resume_strength,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "core_missing": core_missing,
        "sections": sections_status,
        "feedback": feedback,
        "skill_gap_roadmap": skill_gap_roadmap,
        "rewrite_suggestions": rewrite_suggestions
    })

    # ---------------------------
    # 12. Save to Database
    # ---------------------------
    try:
        save_result(
            candidate_name=candidate_name,
            resume_text=resume_text,
            job_description=job_description,
            score=ats_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )
    except Exception as e:
        logging.warning(f"Database save failed: {e}")

    return result
