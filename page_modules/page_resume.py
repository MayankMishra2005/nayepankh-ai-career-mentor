# =============================================================================
# pages/page_resume.py  –  Resume Analyzer with parsed sub-scores & visual bars
# =============================================================================

import streamlit as st
import re
import utils.memory as memory
from ui.components import section_header, divider, score_card, warning_box, progress_bar, info_box, success_box
from modules.resume_analyzer import render_resume_upload, analyze_resume


def parse_resume_breakdown(text: str) -> dict:
    """
    Parse section sub-scores from the AI markdown response table.
    """
    sections = [
        "Contact Information",
        "Summary/Objective",
        "Education",
        "Skills Section",
        "Experience/Projects",
        "Formatting & ATS"
    ]
    scores = {}
    for sec in sections:
        # Match lines like | Contact Information | 8/10 | ...
        match = re.search(rf'\|\s*{re.escape(sec)}\s*\|\s*(\d+)\s*/\s*(\d+)', text, re.IGNORECASE)
        if match:
            scores[sec] = {
                "score": int(match.group(1)),
                "max": int(match.group(2))
            }
    return scores


def parse_resume_sections(text: str) -> dict:
    """
    Split major sections like Strengths, Missing Sections, Suggestions, etc.
    """
    sections = {}
    matches = list(re.finditer(r'## ([^\n]+)\n', text))
    for idx, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[idx+1].start() if idx + 1 < len(matches) else len(text)
        sections[title] = text[start:end].strip()
    return sections


def render():
    st.markdown("""
    <div class="animate-in">
      <h2 style="margin-bottom:0.2rem; font-family:'Space Grotesk', sans-serif;">📄 Resume ATS Reviewer</h2>
      <p style="color:#64748B;margin-top:0;font-size:0.95rem;">
        Upload your PDF resume to receive a comprehensive ATS check, sub-score breakdown, and optimization tips.
      </p>
    </div>
    """, unsafe_allow_html=True)

    profile = memory.get_profile()
    divider()

    # ── Upload Widget ──────────────────────────────────────────────────────
    section_header("Upload Resume File", "📤")
    resume_text, uploaded_file = render_resume_upload()

    cached = memory.get("resume_analysis")
    cached_score = memory.get("resume_score", 0)

    if resume_text:
        analyze_btn = st.button(
            "🔍 Start Resume Audit",
            type="primary",
            use_container_width=True,
            key="analyze_resume_btn",
        )
        if analyze_btn:
            with st.spinner("🤖 Simulating ATS scanning and parsing sections..."):
                result, score = analyze_resume(resume_text, profile)
            cached = result
            cached_score = score
            st.rerun()

    # ── Display Audit Results ──────────────────────────────────────────────
    if cached:
        divider()
        section_header("Resume Audit Results", "📊")

        # Top level widgets
        c1, c2, c3 = st.columns(3)
        with c1:
            score_card("Overall Resume Score", cached_score, "📄")
        with c2:
            label = "Excellent" if cached_score >= 80 else ("Average" if cached_score >= 55 else "Critical Gaps")
            score_card("Recruiter Evaluation", cached_score, "⭐")
        with c3:
            ats_score = min(cached_score + 4, 100)
            score_card("ATS Match Probability", ats_score, "🤖")

        divider()

        # Parse sub-scores table
        subscores = parse_resume_breakdown(cached)
        
        col_l, col_r = st.columns([1, 1])
        
        with col_l:
            section_header("Section Sub-Scores Breakdown", "📊")
            if subscores:
                st.markdown("""
                <div class="np-card" style="padding:1.5rem;">
                """, unsafe_allow_html=True)
                for sec_name, data in subscores.items():
                    color = "#10B981" if data["score"] >= (data["max"] * 0.75) else ("#F59E0B" if data["score"] >= (data["max"] * 0.5) else "#EF4444")
                    progress_bar(sec_name, data["score"], data["max"], color=color)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                info_box("Sub-score table could not be parsed. See markdown below for details.")

        with col_r:
            # Parse text sections
            parsed_sections = parse_resume_sections(cached)
            
            section_header("Audit Summary & Actions", "📋")
            
            # Find matching sections
            red_flags_title = [k for k in parsed_sections.keys() if "Missing" in k or "Red Flags" in k]
            suggested_summary_title = [k for k in parsed_sections.keys() if "Summary" in k or "Objective" in k]
            
            if red_flags_title:
                st.markdown(f"<p style='font-weight:700; color:#EF4444; margin-bottom:0.3rem;'>⚠️ Red Flags & Missing Elements</p>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="np-card" style="border-left:4px solid var(--danger); padding:1rem 1.25rem;">
                  <div style="font-size:0.88rem; line-height:1.5; color:#475569;">
                """, unsafe_allow_html=True)
                st.markdown(parsed_sections[red_flags_title[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)
                
            if suggested_summary_title:
                st.markdown(f"<p style='font-weight:700; color:#8B5CF6; margin: 1rem 0 0.3rem;'>📝 Recommended ATS Summary Statement</p>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="np-card" style="border-left:4px solid var(--secondary); padding:1rem 1.25rem;">
                  <div style="font-size:0.88rem; line-height:1.5; color:#475569; font-style:italic;">
                """, unsafe_allow_html=True)
                st.markdown(parsed_sections[suggested_summary_title[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)

        divider()
        section_header("Full Structured Suggestions Details", "🔍")
        
        # Display full feedback
        st.markdown("""
        <div class="np-card np-card-glow-blue" style="padding:1.75rem;">
        """, unsafe_allow_html=True)
        st.markdown(cached)
        st.markdown("</div>", unsafe_allow_html=True)

        divider()
        st.download_button(
            label="📥 Download Detailed Audit Report (.md)",
            data=cached,
            file_name="resume_audit_report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    elif not resume_text:
        st.markdown("""
        <div class="np-info-box animate-in" style="text-align:center; padding:2.5rem; justify-content:center; flex-direction:column;">
          <div style="font-size:3rem; margin-bottom:0.8rem;">📄</div>
          <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.2rem; color:#1E40AF;">Upload your PDF resume to start</div>
          <div style="font-size:0.9rem; color:#3B82F6; margin-top:0.3rem;">
            Ensure the document is a readable PDF format under 10 MB.
          </div>
        </div>
        """, unsafe_allow_html=True)
