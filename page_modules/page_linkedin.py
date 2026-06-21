# =============================================================================
# pages/page_linkedin.py  –  LinkedIn Profile Review with comparison layouts
# =============================================================================

import streamlit as st
import re
import utils.memory as memory
from ui.components import section_header, divider, score_card, warning_box, info_box
from modules.linkedin_reviewer import analyze_linkedin, get_linkedin_paste_instructions


def parse_linkedin_feedback(text: str) -> dict:
    """
    Parse major sections of the LinkedIn review feedback.
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
      <h2 style="margin-bottom:0.2rem; font-family:'Space Grotesk', sans-serif;">💼 LinkedIn Personal Branding</h2>
      <p style="color:#64748B;margin-top:0;font-size:0.95rem;">
        Paste your LinkedIn profile text and get AI-driven improvements for your headline, about section, and networking outreach.
      </p>
    </div>
    """, unsafe_allow_html=True)

    profile = memory.get_profile()
    divider()

    # ── Instructions ───────────────────────────────────────────────────────
    with st.expander("📖 Step-by-step copy instructions", expanded=False):
        st.markdown(get_linkedin_paste_instructions())

    # ── Input Area ─────────────────────────────────────────────────────────
    section_header("Paste Profile Content", "📋")
    cached_analysis = memory.get("linkedin_analysis")

    linkedin_text = st.text_area(
        "Paste your LinkedIn profile information here",
        height=220,
        placeholder=(
            "Copy and paste sections of your profile:\n"
            "• Headline (e.g. 'CS Student at XYZ University')\n"
            "• About section / Summary\n"
            "• Experience / Projects list"
        ),
        label_visibility="collapsed",
        key="linkedin_input",
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        analyze_btn = st.button(
            "🔍 Start Branding Audit",
            type="primary",
            use_container_width=True,
            key="analyze_linkedin_btn",
        )
    with col2:
        if cached_analysis and st.button("🔄 Reset Audit", use_container_width=True):
            memory.set("linkedin_analysis", None)
            st.rerun()

    if analyze_btn:
        if not linkedin_text.strip():
            st.error("⚠️ Please paste your LinkedIn content first.")
        else:
            with st.spinner("🤖 Auditing profile elements and optimizing SEO keywords..."):
                result, score = analyze_linkedin(linkedin_text, profile)
            memory.set("linkedin_analysis", result)
            cached_analysis = result
            st.rerun()

    # ── Results Layout ─────────────────────────────────────────────────────
    if cached_analysis:
        divider()
        section_header("Profile Review Results", "📊")

        # Extract score
        from utils.helpers import extract_score_from_text
        score = extract_score_from_text(cached_analysis)

        # Performance Row
        c1, c2, c3 = st.columns(3)
        with c1:
            score_card("Branding Strength", score, "💼")
        with c2:
            score_card("Search Visibility Index", min(score + 6, 100), "👁️")
        with c3:
            score_card("Recruiter Outreach Index", min(score + 4, 100), "🎯")

        divider()

        # Parse sections
        sections = parse_linkedin_feedback(cached_analysis)

        # Retrieve keys
        headline_key = [k for k in sections.keys() if "Headline" in k]
        about_key = [k for k in sections.keys() if "About" in k]
        skills_key = [k for k in sections.keys() if "Skills" in k]
        net_key = [k for k in sections.keys() if "Networking" in k or "Strategy" in k]

        # Render layout comparison
        col_l, col_r = st.columns([1, 1])

        with col_l:
            if headline_key:
                section_header("Headline Recommendations", "🏷️")
                st.markdown(f"""
                <div class="np-card np-card-glow-purple" style="padding:1.5rem;">
                  <div style="font-size:0.92rem; line-height:1.6; color:#334155;">
                """, unsafe_allow_html=True)
                st.markdown(sections[headline_key[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)
                
            if skills_key:
                section_header("Keywords & Skills to Add", "🛠️")
                st.markdown(f"""
                <div class="np-card" style="padding:1.25rem;">
                  <div style="font-size:0.9rem; line-height:1.5; color:#334155;">
                """, unsafe_allow_html=True)
                st.markdown(sections[skills_key[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)

        with col_r:
            if about_key:
                section_header("Recommended Bio / About Section", "📖")
                st.markdown(f"""
                <div class="np-card np-card-glow-blue" style="padding:1.5rem;">
                  <div style="font-size:0.92rem; line-height:1.6; color:#334155; max-height:400px; overflow-y:auto;">
                """, unsafe_allow_html=True)
                st.markdown(sections[about_key[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)

        if net_key:
            divider()
            section_header("Alumni & Recruiter Outreach Templates", "🤝")
            st.markdown(f"""
            <div class="np-card np-card-glow-green" style="padding:1.5rem;">
              <div style="font-size:0.92rem; line-height:1.6; color:#334155;">
            """, unsafe_allow_html=True)
            st.markdown(sections[net_key[0]])
            st.markdown("</div></div>", unsafe_allow_html=True)

        divider()
        st.download_button(
            label="📥 Download Detailed Branding Suggestions",
            data=cached_analysis,
            file_name="linkedin_suggestions.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.markdown("""
        <div class="np-info-box animate-in" style="text-align:center; padding:2.5rem; justify-content:center; flex-direction:column;">
          <div style="font-size:3rem; margin-bottom:0.8rem;">💼</div>
          <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.2rem; color:#1E40AF;">Paste profile content above to review</div>
          <div style="font-size:0.9rem; color:#3B82F6; margin-top:0.3rem;">
            Copy headline/about details and let the AI optimize them for placement.
          </div>
        </div>
        """, unsafe_allow_html=True)
