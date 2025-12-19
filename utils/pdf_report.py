from fpdf import FPDF
from datetime import datetime

def generate_pdf(candidate_name, match_score, skills, missing_keywords, experience, file_path="resume_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Resume Analyzer Report - {candidate_name}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, f"Match Score: {match_score}%")
    pdf.ln(5)

    pdf.multi_cell(0, 8, f"Skills Found: {', '.join(skills) if skills else 'None'}")
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Missing Keywords: {', '.join(missing_keywords) if missing_keywords else 'None'}")
    pdf.ln(5)

    if experience:
        pdf.multi_cell(0, 8, "Relevant Experience:")
        for exp in experience:
            pdf.multi_cell(0, 8, f" - {exp}")
    else:
        pdf.multi_cell(0, 8, "Relevant Experience: None")
    pdf.ln(10)

    pdf.multi_cell(0, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    pdf.output(file_path)
    return file_path
