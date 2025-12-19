# resume_analyzer/utils/parser.py

def parse_resume(file_path):
    """
    Dummy parser that reads a text file and extracts basic info.
    Replace this with actual PDF/Word parsing if needed.
    """
    resume_data = {"name": "", "email": "", "skills": []}

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line.lower().startswith("name:"):
            resume_data["name"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("email:"):
            resume_data["email"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("skills:"):
            skills_str = line.split(":", 1)[1].strip()
            resume_data["skills"] = [s.strip() for s in skills_str.split(",")]

    return resume_data
