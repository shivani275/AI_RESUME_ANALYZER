# utils/llm_rewriter.py

from typing import List, Dict
import logging
import os

from .rewrite_templates import generate_rewrite_suggestions

# ---------------------------
# Check GPT4All availability
# ---------------------------
try:
    from gpt4all import GPT4All
    GPT4ALL_AVAILABLE = True
except ImportError:
    logging.warning("GPT4All not installed. Falling back to static templates.")
    GPT4ALL_AVAILABLE = False

MODEL_PATH = os.path.join("models", "ggml-gpt4all-j.bin")

SYSTEM_PROMPT = """
You are an expert technical recruiter and ATS optimization specialist.
Rewrite resume bullet points to:
- Be ATS-friendly
- Use strong action verbs
- Be concise and professional
- Include measurable impact where possible
Return ONE bullet point per skill.
"""

def llm_rewrite_skills(skills: List[str], job_description: str) -> List[Dict[str, str]]:
    """
    Generate ATS-optimized rewrite suggestions using GPT4All if available.
    Falls back to static templates otherwise.

    Args:
        skills (List[str]): List of skills to rewrite.
        job_description (str): Context of job description for tailoring.

    Returns:
        List[Dict[str, str]]: Each dict contains:
            - skill: str
            - suggested_rewrite: str
            - recommended_section: str
            - source: "gpt4all" or "template"
    """
    if not skills:
        return []

    # Fallback to templates if GPT4All unavailable or model file missing
    if not GPT4ALL_AVAILABLE or not os.path.exists(MODEL_PATH):
        suggestions = generate_rewrite_suggestions(skills)
        # Add source field for consistency
        for s in suggestions:
            s["source"] = "template"
        return suggestions

    try:
        # Instantiate GPT4All model
        model = GPT4All(model_name=MODEL_PATH)
        results: List[Dict[str, str]] = []

        for skill in skills:
            prompt = (
                f"{SYSTEM_PROMPT}\nSkill: {skill}\nJob Description Context: {job_description}\n"
            )
            response = model.generate(prompt, max_tokens=100)
            results.append({
                "skill": skill,
                "suggested_rewrite": response.strip(),
                "recommended_section": "Experience / Projects",
                "source": "gpt4all"
            })

        return results

    except Exception as e:
        logging.warning(f"GPT4All generation failed: {e}")
        # Fallback to static templates in case of error
        suggestions = generate_rewrite_suggestions(skills)
        for s in suggestions:
            s["source"] = "template"
        return suggestions
