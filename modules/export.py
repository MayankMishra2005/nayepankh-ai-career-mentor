# =============================================================================
# modules/export.py
# Generate a downloadable PDF report of the student's full career analysis.
# =============================================================================

from fpdf import FPDF
import streamlit as st
import utils.memory as memory
from datetime import datetime
import re


class CareerReportPDF(FPDF):
    """Custom FPDF class for the NayePankh career report."""

    def header(self):
        self.set_fill_color(26, 86, 219)        # Primary blue
        self.rect(0, 0, 210, 18, 'F')
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 4)
        self.cell(0, 10, "NayePankh Career Mentor Report", align="L")
        self.set_xy(10, 4)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 10, datetime.now().strftime("%d %b %Y"), align="R")
        self.ln(14)
        self.set_text_color(30, 41, 59)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, f"Page {self.page_no()} | NayePankh Foundation — Career Mentor AI", align="C")

    def chapter_title(self, title: str, color: tuple = (26, 86, 219)):
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 9, f"  {title}", ln=True, fill=True)
        self.set_text_color(30, 41, 59)
        self.ln(2)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 41, 59)
        # Strip markdown symbols for clean PDF output
        clean = _strip_markdown(text)
        # Split into lines and write
        for line in clean.split("\n"):
            line = line.strip()
            if not line:
                self.ln(2)
                continue
            # Bold headings (lines starting with ##)
            if line.startswith("##"):
                self.set_font("Helvetica", "B", 10)
                self.set_text_color(26, 86, 219)
                self.multi_cell(0, 6, line.lstrip("#").strip())
                self.set_font("Helvetica", "", 9)
                self.set_text_color(30, 41, 59)
            elif line.startswith("#"):
                self.set_font("Helvetica", "B", 11)
                self.set_text_color(124, 58, 237)
                self.multi_cell(0, 7, line.lstrip("#").strip())
                self.set_font("Helvetica", "", 9)
                self.set_text_color(30, 41, 59)
            else:
                self.multi_cell(0, 5.5, line)
        self.ln(3)


def _strip_markdown(text: str) -> str:
    """Remove common markdown symbols for plain-text PDF output."""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # bold
    text = re.sub(r'\*(.*?)\*',     r'\1', text)    # italic
    text = re.sub(r'`(.*?)`',       r'\1', text)    # inline code
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)     # images
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # links
    return text


def generate_pdf_report() -> bytes | None:
    """
    Build a full PDF report from all session state data.

    Returns:
        PDF bytes if successful, None otherwise.
    """
    profile        = memory.get_profile()
    agent_outputs  = memory.get("agent_outputs", {})
    resume_score   = memory.get("resume_score", 0)
    intern_score   = memory.get("internship_score", 0)
    resume_text    = memory.get("resume_analysis", "")
    linkedin_text  = memory.get("linkedin_analysis", "")
    skill_gap_text = memory.get("skill_gap_analysis", "")

    pdf = CareerReportPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    # ── Cover Section ────────────────────────────────────────────────────────
    pdf.set_fill_color(240, 249, 255)
    pdf.set_draw_color(191, 219, 254)
    pdf.rect(10, 22, 190, 36, 'FD')
    pdf.set_xy(14, 25)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(26, 86, 219)
    pdf.cell(0, 9, f"Career Analysis Report", ln=True)
    pdf.set_xy(14, 34)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 7, f"Student: {profile.get('name', 'N/A')}", ln=True)
    pdf.set_xy(14, 41)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(0, 6, f"{profile.get('degree','')} | {profile.get('branch','')} | {profile.get('year','')}", ln=True)
    pdf.ln(20)

    # ── Scores Summary ───────────────────────────────────────────────────────
    pdf.chapter_title("📊 Score Summary", color=(26, 86, 219))
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(95, 8, f"Resume Score:            {resume_score}/100", ln=False)
    pdf.cell(95, 8, f"Internship Readiness:    {intern_score}/100", ln=True)
    pdf.cell(95, 8, f"Career Goal:             {profile.get('career_goal','N/A')}", ln=False)
    pdf.cell(95, 8, f"Target Industry:         {profile.get('industry','N/A')}", ln=True)
    pdf.ln(4)

    # ── Student Profile ──────────────────────────────────────────────────────
    pdf.chapter_title("👤 Student Profile", color=(26, 86, 219))
    for label, key in [
        ("Name", "name"), ("Degree", "degree"), ("Branch", "branch"),
        ("Year", "year"), ("Skills", "skills"), ("Interests", "interests"),
        ("Career Goal", "career_goal"), ("Industry", "industry"),
    ]:
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(45, 6, f"{label}:", ln=False)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 6, str(profile.get(key, "N/A")))
    pdf.ln(3)

    # ── Agent Outputs ─────────────────────────────────────────────────────────
    agent_map = [
        ("profile_analyzer",   "🧠 Profile Analysis",       (26, 86, 219)),
        ("career_mentor",      "🎯 Career Recommendations",  (124, 58, 237)),
        ("learning_roadmap",   "🗺️ Learning Roadmap",        (5, 150, 105)),
        ("project_recommender","🏗️ Project Recommendations",  (217, 119, 6)),
        ("internship_readiness","💼 Internship Readiness",   (37, 99, 235)),
        ("motivation_guidance","🌟 Motivation & Guidance",   (124, 58, 237)),
    ]

    for key, title, color in agent_map:
        content = agent_outputs.get(key, {})
        if isinstance(content, dict):
            content = content.get("content", "")
        if content and not content.startswith("⚠️"):
            pdf.add_page()
            pdf.chapter_title(title, color=color)
            pdf.body_text(content)

    # ── Resume Analysis ───────────────────────────────────────────────────────
    if resume_text and not resume_text.startswith("⚠️"):
        pdf.add_page()
        pdf.chapter_title("📄 Resume Analysis", color=(5, 150, 105))
        pdf.body_text(resume_text)

    # ── LinkedIn Review ────────────────────────────────────────────────────────
    if linkedin_text and not linkedin_text.startswith("⚠️"):
        pdf.add_page()
        pdf.chapter_title("💼 LinkedIn Review", color=(26, 86, 219))
        pdf.body_text(linkedin_text)

    # ── Skill Gap ──────────────────────────────────────────────────────────────
    if skill_gap_text and not skill_gap_text.startswith("⚠️"):
        pdf.add_page()
        pdf.chapter_title("📊 Skill Gap Analysis", color=(217, 119, 6))
        pdf.body_text(skill_gap_text)

    return bytes(pdf.output())


def render_export_button():
    """Render a Streamlit download button for the PDF report."""
    st.markdown("### 📥 Export Your Career Report")
    st.markdown("Download a complete PDF report of all AI-generated insights.")

    if st.button("🖨️ Generate & Download PDF Report", type="primary", use_container_width=True):
        with st.spinner("📑 Generating your personalised report..."):
            pdf_bytes = generate_pdf_report()

        if pdf_bytes:
            profile = memory.get_profile()
            name    = profile.get("name", "Student").replace(" ", "_")
            date    = datetime.now().strftime("%Y%m%d")
            filename = f"NayePankh_Career_Report_{name}_{date}.pdf"

            st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True,
            )
            st.success("✅ Report generated successfully! Click above to download.")
        else:
            st.error("❌ Could not generate report. Please ensure you have run at least one AI agent first.")
