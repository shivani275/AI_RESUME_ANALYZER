"""
rewrite_templates.py
--------------------
Rule-based ATS-friendly rewrite templates
(Fallback when LLM is unavailable)
"""

from typing import List, Dict

# --------------------------------------------------
# Canonical ATS Rewrite Templates
# --------------------------------------------------
REWRITE_TEMPLATES = {
    "python": (
        "Developed backend applications using Python to build scalable, "
        "maintainable, and high-performance systems."
    ),
    "sql": (
        "Designed, optimized, and maintained SQL queries to analyze large datasets "
        "and improve database performance."
    ),
    "machine learning": (
        "Built and deployed machine learning models to automate predictions "
        "and support data-driven decision-making."
    ),
    "docker": (
        "Containerized applications using Docker to ensure consistent environments "
        "across development, testing, and production."
    ),
    "aws": (
        "Deployed and managed cloud-based applications on AWS using services "
        "such as EC2, S3, and IAM."
    ),
    "rest api": (
        "Designed and implemented RESTful APIs to enable secure and efficient "
        "communication between services."
    ),
    "nlp": (
        "Applied natural language processing techniques to extract insights "
        "from unstructured text data."
    ),
    "data analysis": (
        "Performed data analysis using Python to identify trends, patterns, "
        "and actionable business insights."
    ),
    "git": (
        "Used Git for version control, collaborating with teams through "
        "branching, merging, and code reviews."
    ),
}

# --------------------------------------------------
# Rewrite Suggestion Generator
# --------------------------------------------------
def generate_rewrite_suggestions(
    missing_skills: List[str],
    section: str = "Experience / Projects"
) -> List[Dict[str, str]]:
    """
    Generate ATS-optimized rewrite suggestions for missing skills.

    Args:
        missing_skills (List[str]): Skills missing from the resume.
        section (str): Recommended resume section.

    Returns:
        List[Dict[str, str]]
    """

    suggestions: List[Dict[str, str]] = []

    if not missing_skills:
        return suggestions

    for skill in missing_skills:
        if not isinstance(skill, str):
            continue

        skill_clean = skill.strip().lower()
        if not skill_clean:
            continue

        # Use canonical template or fallback
        rewrite = REWRITE_TEMPLATES.get(
            skill_clean,
            (
                f"Applied {skill_clean.title()} in real-world projects to "
                "solve practical problems and deliver measurable results."
            )
        )

        suggestions.append({
            "skill": skill_clean,
            "suggested_rewrite": rewrite,
            "recommended_section": section
        })

    return suggestions
