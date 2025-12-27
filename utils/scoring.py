# utils/scoring.py
from typing import List, Tuple


def calculate_match_score(
    resume_skills: List[str],
    jd_skills: List[str]
) -> Tuple[int, List[str], List[str]]:
    """
    Pure ATS-style scoring (rule-based)

    Returns:
    - ATS score (0–100)
    - matched skills
    - missing skills
    """

    # Defensive normalization
    resume_set = set(map(str.lower, resume_skills or []))
    jd_set = set(map(str.lower, jd_skills or []))

    matched_skills = sorted(resume_set & jd_set)
    missing_skills = sorted(jd_set - resume_set)

    # Avoid division errors
    if not jd_set:
        return 0, matched_skills, missing_skills

    # ATS score: % of JD skills found
    score = int(round((len(matched_skills) / len(jd_set)) * 100))

    return score, matched_skills, missing_skills


def calculate_resume_strength(
    resume_text: str,
    resume_skills: List[str]
) -> int:
    """
    Resume quality score (ATS formatting proxy)

    Factors:
    - Resume length
    - Skill density
    """

    if not resume_text:
        return 0

    word_count = len(resume_text.split())
    skill_count = len(resume_skills or [])

    # Length scoring (ideal ≈ 500–600 words)
    length_score = min(word_count / 600, 1.0)

    # Skill density scoring (ideal ≈ 15–20 skills)
    skill_score = min(skill_count / 20, 1.0)

    # Heavy penalty for very short resumes
    if word_count < 250:
        length_score *= 0.6

    strength = (0.6 * length_score) + (0.4 * skill_score)

    return int(round(strength * 100))
