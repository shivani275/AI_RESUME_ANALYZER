# resume_analyzer/main.py

"""
CLI entry point for testing core Resume Analyzer logic
(without Streamlit UI).

Useful for:
- Debugging
- Unit testing
- Validating core logic
"""

from pathlib import Path
from resume_analyzer.utils import analyze_resume


def main():
    resume_file_path = Path("examples/sample_resume.pdf")
    job_description_path = Path("examples/sample_jd.txt")

    print("📄 Running Resume Analyzer (CLI mode)\n")

    if not resume_file_path.exists():
        print("❌ Resume file not found:", resume_file_path)
        return

    if not job_description_path.exists():
        print("❌ Job description file not found:", job_description_path)
        return

    try:
        # Read Job Description
        job_description = job_description_path.read_text(encoding="utf-8")

        # Open resume as binary (same as Streamlit uploader)
        with resume_file_path.open("rb") as resume_file:
            result = analyze_resume(
                resume_file=resume_file,
                job_description=job_description,
                candidate_name="CLI Candidate"
            )

        if not result:
            print("❌ Analysis failed. No result returned.")
            return

        # ---------------------------
        # Output Results
        # ---------------------------
        print(f"\n✅ Match Score: {result.get('match_score', 0)}%")
        print(f"💪 Resume Strength: {result.get('resume_strength', 0)}%\n")

        # Matched Skills
        matched_skills = result.get("matched_skills", [])
        print("🧠 Matched Skills:")
        if matched_skills:
            for skill in matched_skills:
                print(f"  ✔ {skill}")
        else:
            print("  None")

        # Missing Skills
        missing_skills = result.get("missing_skills", [])
        print("\n❌ Missing Skills:")
        if missing_skills:
            for skill in missing_skills:
                print(f"  ✖ {skill}")
        else:
            print("  None")

        # Resume Sections
        sections = result.get("sections", {})
        print("\n📌 Resume Sections:")
        if sections:
            for section, present in sections.items():
                status = "✔" if present else "✖"
                print(f"  {status} {section.title()}")
        else:
            print("  No sections detected")

        # Feedback
        feedback = result.get("feedback", [])
        print("\n🛠 Feedback:")
        if feedback:
            for tip in feedback:
                print(f"  • {tip}")
        else:
            print("  No feedback generated")

        # PDF report
        pdf_path = result.get("pdf_path")
        if pdf_path:
            print(f"\n📄 PDF Report Generated: {pdf_path}")
        else:
            print("\n❌ PDF report not generated")

    except Exception as e:
        print(f"\n❌ Error running analyzer: {e}")


if __name__ == "__main__":
    main()
