# utils/skill_gap.py
from typing import Dict, List


# --------------------------------------------------
# ATS Skill Priority Buckets (canonical lowercase)
# --------------------------------------------------
CORE_SKILLS = {
    "python", "java", "javascript", "sql",
    "data analysis", "machine learning",
    "oop", "git", "rest api"
}

SECONDARY_SKILLS = {
    "pandas", "numpy", "excel",
    "docker", "aws", "flask", "django",
    "react", "nlp"
}


def generate_skill_gap_roadmap(
    jd_skills: List[str],
    resume_skills: List[str]
) -> Dict[str, List[str]]:
    """
    Generate an ATS-style skill gap learning roadmap.

    Priority:
    - critical   → Core ATS blockers
    - important  → Strong ATS boosters
    - optional   → Nice-to-have skills
    """

    # Defensive programming
    jd_set = set(map(str.lower, jd_skills or []))
    resume_set = set(map(str.lower, resume_skills or []))

    missing_skills = jd_set - resume_set

    roadmap: Dict[str, List[str]] = {
        "critical": [],
        "important": [],
        "optional": []
    }

    for skill in sorted(missing_skills):
        if skill in CORE_SKILLS:
            roadmap["critical"].append(skill)
        elif skill in SECONDARY_SKILLS:
            roadmap["important"].append(skill)
        else:
            roadmap["optional"].append(skill)

    return roadmap
