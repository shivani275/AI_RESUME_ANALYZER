# utils/skill_extractor.py
from typing import List, Set
import re
from .nlp_processing import clean_text

# ---------------------------
# Canonical skills and synonyms
# ---------------------------
SKILL_SYNONYMS = {
    "python": ["python"],
    "java": ["java"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "excel": ["excel", "spreadsheets", "ms excel"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics", "data analyst"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "communication": ["communication", "presentations", "verbal communication"],
    "teamwork": ["teamwork", "collaboration", "cross functional"]
}


def extract_skills(text: str) -> List[str]:
    """
    Extract normalized skills from text using robust word-boundary matching.
    Returns canonical skill names only (ATS-friendly).

    Args:
        text (str): Resume or job description text.

    Returns:
        List[str]: Sorted list of canonical skills found in text.
    """

    if not isinstance(text, str) or not text.strip():
        return []

    # Clean & normalize text
    text_clean = clean_text(text)

    found_skills: Set[str] = set()

    for canonical_skill, variants in SKILL_SYNONYMS.items():
        for variant in variants:
            # Strict word-boundary match (prevents false positives)
            pattern = rf"\b{re.escape(variant.lower())}\b"
            if re.search(pattern, text_clean):
                found_skills.add(canonical_skill)
                break  # Stop after first match per skill

    return sorted(found_skills)
