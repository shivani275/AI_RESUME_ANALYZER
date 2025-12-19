def validate_resume_for_job(resume_skills, required_skills):
    """
    Check if resume contains all required job skills.
    Returns:
        valid (bool): True if all required skills are present
        missing (list): list of missing skills
    """
    missing = [skill for skill in required_skills if skill.lower() not in [s.lower() for s in resume_skills]]
    valid = len(missing) == 0
    return valid, missing
