# =============================================================================
# pages/page_skillgap.py  –  Skill Gap Analysis with tabbed layout
# =============================================================================

import streamlit as st
import re
import utils.memory as memory
from ui.components import section_header, divider, skill_tags, warning_box, info_box, premium_metric_card
from modules.skill_gap import run_skill_gap_analysis
from utils.helpers import parse_skills_list
from config.settings import INDUSTRIES


def parse_skill_gap_report(text: str) -> dict:
    """
    Parse the skill gap analysis sections dynamically using H2 headers.
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
      <h2 style="margin-bottom:0.2rem; font-family:'Space Grotesk', sans-serif;">📊 Skill Gap Analysis</h2>
      <p style="color:#64748B;margin-top:0;font-size:0.95rem;">
        Assess your technical gap against your target position and discover priority items to study.
      </p>
    </div>
    """, unsafe_allow_html=True)

    profile = memory.get_profile()
    divider()

    # ── Configuration Form ──────────────────────────────────────────────────
    section_header("Configure Assessment Criteria", "⚙️")
    col1, col2 = st.columns(2)

    with col1:
        current_skills_input = st.text_area(
            "Your Current Skills",
            value=profile.get("skills", ""),
            height=120,
            placeholder="e.g. Python, SQL, Git, Excel, Communication, Teamwork",
            help="List your skills separated by commas",
        )

    with col2:
        target_career = st.text_input(
            "Target Career / Role",
            value=profile.get("career_goal", ""),
            placeholder="e.g. Data Scientist at a product company",
        )
        target_industry = st.selectbox(
            "Target Industry",
            options=INDUSTRIES,
            index=INDUSTRIES.index(profile.get("industry", INDUSTRIES[0]))
            if profile.get("industry") in INDUSTRIES else 0,
        )

    cached_analysis = memory.get("skill_gap_analysis")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        run_btn = st.button(
            "🔍 Analyze Skill Gap Now",
            type="primary",
            use_container_width=True,
            key="run_skillgap_btn",
        )
    with col_b:
        if cached_analysis and st.button("🔄 Reset Report", use_container_width=True):
            memory.set("skill_gap_analysis", None)
            st.rerun()

    if run_btn:
        if not target_career.strip():
            st.error("⚠️ Please specify a target career role.")
        else:
            # Sync skills back to profile if modified
            if current_skills_input.strip() != profile.get("skills", ""):
                memory.update_profile("skills", current_skills_input.strip())

            with st.spinner("🤖 Mapping skill requirements and gaps..."):
                result = run_skill_gap_analysis(
                    profile, target_career, target_industry
                )
            memory.set("skill_gap_analysis", result)
            cached_analysis = result
            st.rerun()

    # ── Current Skills Visual ──────────────────────────────────────────────
    if current_skills_input:
        divider()
        section_header("Your Current Skills Inventory", "🛠️")
        skills_list = parse_skills_list(current_skills_input)
        if skills_list:
            skill_tags(skills_list, color="#10B981")
            st.markdown(
                f'<p style="font-size:0.85rem;color:#64748B;margin-top:0.6rem;font-weight:600;">'
                f'✓ Total of {len(skills_list)} skills registered</p>',
                unsafe_allow_html=True,
            )

    # ── Analysis Results (Tabbed Breakdown) ────────────────────────────────
    if cached_analysis:
        divider()
        section_header("AI Skill Gap Intelligence Report", "📋")

        sections = parse_skill_gap_report(cached_analysis)

        # Draw summary indicators
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            premium_metric_card("Critical Gaps", "🚨 Gaps Found", "Require immediate attention", "🚨", "#EF4444")
        with sc2:
            premium_metric_card("High Priority", "⚡ Gaps Found", "Study for interviews", "⚡", "#F59E0B")
        with sc3:
            premium_metric_card("Competitive Edge", "📚 Electives", "Secondary nice-to-haves", "📚", "#10B981")

        divider()

        # Render parsed sections in tabs
        tab_critical, tab_high, tab_learning, tab_resources = st.tabs([
            "🚨 Critical Gaps",
            "⚡ High Priority",
            "🗺️ Learning Order & Time",
            "🎓 Course Resources",
        ])

        # Match keys from config settings
        critical_key = [k for k in sections.keys() if "Critical" in k]
        high_key = [k for k in sections.keys() if "High Priority" in k]
        nice_key = [k for k in sections.keys() if "Nice-to-Have" in k]
        order_key = [k for k in sections.keys() if "Priority Order" in k or "Sequence" in k]
        time_key = [k for k in sections.keys() if "Time to Close" in k or "Timeline" in k]
        resources_key = [k for k in sections.keys() if "Resources" in k]

        with tab_critical:
            st.markdown("These skills are critical gating factors blocking you from entry-level positions.")
            if critical_key:
                st.markdown(f"""
                <div class="np-card np-card-glow-purple" style="padding:1.5rem;">
                  <div style="font-size:0.92rem; line-height:1.6; color:#334155;">
                """, unsafe_allow_html=True)
                st.markdown(sections[critical_key[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                info_box("No critical gaps identified.")

        with tab_high:
            st.markdown("These skills will help you stand out and clear technical placement interviews.")
            if high_key:
                st.markdown(f"""
                <div class="np-card np-card-glow-blue" style="padding:1.5rem;">
                  <div style="font-size:0.92rem; line-height:1.6; color:#334155;">
                """, unsafe_allow_html=True)
                st.markdown(sections[high_key[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                info_box("No high priority gaps identified.")
                
            if nice_key:
                st.markdown("<p style='font-weight:700; color:#0F172A; margin: 1rem 0 0.5rem;'>📚 Good-to-Have Skills</p>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="np-card" style="padding:1.25rem;">
                  <div style="font-size:0.9rem; line-height:1.5; color:#334155;">
                """, unsafe_allow_html=True)
                st.markdown(sections[nice_key[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)

        with tab_learning:
            st.markdown("Proposed sequence and timeline to close identified technical gaps.")
            if order_key:
                st.markdown("##### 🗺️ Recommended Study Sequence")
                st.markdown(sections[order_key[0]])
            if time_key:
                st.markdown("<br/>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background:rgba(59, 130, 246, 0.05); border:1px solid rgba(59,130,246,0.15); border-left:4px solid var(--primary);
                            padding:1.25rem; border-radius:12px;">
                  <div style="font-weight:700; font-size:0.95rem; color:#3B82F6; margin-bottom:0.4rem;">⏱️ Estimated Gaps Timeline</div>
                  <div style="font-size:0.9rem; line-height:1.5; color:#334155;">
                """, unsafe_allow_html=True)
                st.markdown(sections[time_key[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)

        with tab_resources:
            st.markdown("Match specific technical skills to structured learning resources and courses.")
            if resources_key:
                st.markdown(f"""
                <div class="np-card np-card-glow-green" style="padding:1.5rem;">
                  <div style="font-size:0.92rem; line-height:1.6; color:#334155;">
                """, unsafe_allow_html=True)
                st.markdown(sections[resources_key[0]])
                st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                info_box("No course matches generated.")

        divider()
        st.download_button(
            label="📥 Download Full Skill Gap Report (.md)",
            data=cached_analysis,
            file_name="skill_gap_analysis.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.markdown("""
        <div class="np-info-box animate-in" style="text-align:center; padding:2.5rem; justify-content:center; flex-direction:column;">
          <div style="font-size:3rem; margin-bottom:0.8rem;">📊</div>
          <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.2rem; color:#1E40AF;">Configure criteria above to run review</div>
          <div style="font-size:0.9rem; color:#3B82F6; margin-top:0.3rem;">
            The AI analyzer will map your skill inventory and prioritize missing key topics.
          </div>
        </div>
        """, unsafe_allow_html=True)
