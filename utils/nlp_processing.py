# utils/nlp_processing.py
import re
from typing import List

# =====================================================
# ATS-Grade Skill Dictionary (expandable)
# =====================================================
SKILL_MAP = {
    # Programming Languages
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "sql": ["sql", "mysql", "postgresql", "sqlite"],

    # Data / Analytics
    "data analysis": ["data analysis"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "statistics": ["statistics"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],

    # Visualization
    "tableau": ["tableau"],
    "power bi": ["power bi"],
    "excel": ["excel"],

    # Web / Backend
    "html": ["html"],
    "css": ["css"],
    "react": ["react", "reactjs"],
    "node.js": ["node.js", "nodejs", "node"],
    "flask": ["flask"],
    "django": ["django"],
    "rest api": ["rest api", "restful api"],

    # DevOps / Cloud
    "aws": ["aws", "amazon web services"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "git": ["git", "github", "gitlab"],
    "ci/cd": ["ci/cd", "continuous integration"],

    # Soft / Business Skills
    "communication": ["communication"],
    "teamwork": ["teamwork", "collaboration"],
    "problem solving": ["problem solving"],
}

# =====================================================
# Text Cleaning
# =====================================================
def clean_text(text: str) -> str:
    """
    ATS-safe text normalization
    - Lowercase
    - Keep letters, digits, +, #, /, ., and spaces
    - Collapse multiple spaces
    """
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#./ ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

# =====================================================
# ATS-Grade Skill Extraction
# =====================================================
def extract_skills(text: str) -> List[str]:
    """
    Deterministic ATS-style skill extraction
    - Exact matching
    - Multi-word support
    - Canonical normalization
    """
    if not text:
        return []

    text_clean = clean_text(text)
    found_skills = set()

    for canonical_skill, variants in SKILL_MAP.items():
        for variant in variants:
            pattern = r"\b" + re.escape(variant) + r"\b"
            if re.search(pattern, text_clean):
                found_skills.add(canonical_skill)
                break

    return sorted(found_skills)

# =====================================================
# Frequency-Based Keyword Extraction (ATS-safe, no ML)
# =====================================================
def extract_keywords(text: str, top_n: int = 15) -> List[str]:
    """
    Simple frequency-based keyword extraction.
    - Ignores stopwords and very short tokens.
    """
    if not text:
        return []

    text_clean = clean_text(text)
    words = text_clean.split()

    stopwords = {
        "and", "or", "the", "with", "to", "for", "of", "in",
        "on", "a", "an", "is", "are", "as", "by", "from"
    }

    freq = {}
    for word in words:
        if word not in stopwords and len(word) > 2:
            freq[word] = freq.get(word, 0) + 1

    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in ranked[:top_n]]
