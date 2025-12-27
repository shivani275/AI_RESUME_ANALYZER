# utils/validator.py
from typing import Dict
import re

# Common required resume sections with header variations
REQUIRED_SECTIONS = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "career summary"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history"
    ],
    "education": [
        "education",
        "academic background",
        "qualifications"
    ],
    "skills": [
        "skills",
        "technical skills",
        "key skills",
        "core competencies"
    ]
}


def validate_resume_sections(resume_text: str) -> Dict[str, bool]:
    """
    Detect resume sections using ATS-style header matching.

    Rules:
    - Section headers must appear at the start of a line
    - Allows punctuation (:, -, —)
    - Case-insensitive
    """

    if not isinstance(resume_text, str) or not resume_text.strip():
        return {section: False for section in REQUIRED_SECTIONS}

    # Normalize text
    text = resume_text.lower()
    text = re.sub(r"\r\n", "\n", text)

    section_status: Dict[str, bool] = {}

    for section, headers in REQUIRED_SECTIONS.items():
        found = False

        for header in headers:
            # Match headers like:
            # "Experience"
            # "Experience:"
            # "EXPERIENCE —"
            pattern = rf"(?m)^\s*{re.escape(header)}\s*[:\-—]?\s*$"

            if re.search(pattern, text):
                found = True
                break

        section_status[section] = found

    return section_status
