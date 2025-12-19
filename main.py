# resume_analyzer/main.py

from resume_analyzer.utils import parser, validator

def main():
    """
    Entry point for the Resume Analyzer project.
    """
    resume_path = "sample_resume.txt"  # Replace with your resume file

    # Step 1: Parse the resume
    try:
        resume_data = parser.parse_resume(resume_path)
        print("Resume parsed successfully!")
        print(resume_data)
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return

    # Step 2: Validate the resume data
    if validator.validate_resume(resume_data):
        print("Resume is valid.")
    else:
        print("Resume is invalid.")
        return

    # Step 3: Analyze (example)
    skills_count = len(resume_data.get("skills", []))
    print(f"Number of skills found: {skills_count}")


if __name__ == "__main__":
    main()
