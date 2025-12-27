from fpdf import FPDF
from datetime import datetime
from pathlib import Path
from typing import List, Union


def _safe_text(text: Union[str, None]) -> str:
    """Ensure text is safe for PDF output."""
    if not text:
        return ""
    return str(text).encode("latin-1", "replace").decode("latin-1")


def generate_pdf(
    candidate_name: str,
    match_score: int,
    skills: List[str],
    missing_keywords: List[str],
    experience: Union[List[str], List[dict]],
    file_path: str = "resume_report.pdf"
) -> str:
    """
    Generate ATS-friendly PDF report (font-safe, no crashes).
    """

    # ---------------------------
    # Font handling (SAFE)
    # ---------------------------
    font_path = Path(__file__).parent / "assets" / "fonts" / "DejaVuSans.ttf"
    use_unicode = font_path.exists()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    if use_unicode:
        pdf.add_font("DejaVu", "", str(font_path), uni=True)
        font = "DejaVu"
    else:
        font = "Helvetica"  # Built-in fallback (NO crash)

    # ---------------------------
    # Title
    # ---------------------------
    pdf.set_font(font, size=20)
    pdf.cell(0, 12, "Resume Analysis Report", ln=True, align="C")
    pdf.ln(6)

    # ---------------------------
    # Candidate Info
    # ---------------------------
    pdf.set_font(font, size=13)
    pdf.cell(0, 10, f"Candidate: {_safe_text(candidate_name)}", ln=True)
    pdf.ln(4)

    # ---------------------------
    # Match Score
    # ---------------------------
    pdf.set_font(font, size=12)
    pdf.cell(0, 8, f"ATS Match Score: {int(match_score)}%", ln=True)
    pdf.ln(6)

    # ---------------------------
    # Skills Found
    # ---------------------------
    pdf.set_font(font, size=13)
    pdf.cell(0, 8, "Matched Skills", ln=True)
    pdf.set_font(font, size=11)
    pdf.multi_cell(0, 7, _safe_text(", ".join(skills) or "None"))
    pdf.ln(4)

    # ---------------------------
    # Missing Skills
    # ---------------------------
    pdf.set_font(font, size=13)
    pdf.cell(0, 8, "Missing / Recommended Skills", ln=True)
    pdf.set_font(font, size=11)
    pdf.multi_cell(0, 7, _safe_text(", ".join(missing_keywords) or "None"))
    pdf.ln(6)

    # ---------------------------
    # Experience Summary
    # ---------------------------
    pdf.set_font(font, size=13)
    pdf.cell(0, 8, "Relevant Experience Summary", ln=True)
    pdf.set_font(font, size=11)

    if experience:
        for i, exp in enumerate(experience, 1):
            if isinstance(exp, dict):
                text = " | ".join(f"{k}: {v}" for k, v in exp.items() if v)
            else:
                text = str(exp)
            pdf.multi_cell(0, 7, f"{i}. {_safe_text(text)}")
    else:
        pdf.multi_cell(0, 7, "No experience data detected.")
    pdf.ln(8)

    # ---------------------------
    # Footer
    # ---------------------------
    pdf.set_font(font, size=9)
    pdf.cell(
        0,
        8,
        f"Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        align="R"
    )

    pdf.output(file_path)
    return file_path
