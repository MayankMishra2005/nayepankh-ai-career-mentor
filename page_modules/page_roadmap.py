# =============================================================================
# pages/page_roadmap.py  –  Career Roadmap with interactive timelines & synced state
# =============================================================================

import streamlit as st
import re
import utils.memory as memory
from ui.components import section_header, divider, warning_box, success_box
from agents.learning_roadmap import run_learning_roadmap
from modules.export import render_export_button


def parse_roadmap_content(text: str):
    """
    Parse month-by-month roadmap sections, certifications, and reference books
    from raw AI markdown output.
    """
    months = []
    certs = ""
    books = ""

    # Locate Month blocks — support en-dash, hyphen, em-dash, or colon after month number
    month_matches = list(re.finditer(
        r'### Month (\d+)\s*(?:–|-|—|:)\s*([^\n]+)', text
    ))
    if month_matches:
        for idx, match in enumerate(month_matches):
            start = match.end()
            end = month_matches[idx+1].start() if idx + 1 < len(month_matches) else len(text)
            
            # Truncate content if it runs into another major H2 section
            h2_match = re.search(r'## ', text[start:end])
            if h2_match:
                end = start + h2_match.start()
                
            months.append({
                "number": int(match.group(1)),
                "title": match.group(2).strip(),
                "content": text[start:end].strip()
            })

    # Extract Certifications section
    certs_match = re.search(r'## 🎓 Certifications to Pursue\s*\n(.*?)(?=##|$)', text, re.DOTALL | re.IGNORECASE)
    if certs_match:
        certs = certs_match.group(1).strip()
    else:
        # Fallback search if title differs slightly
        certs_match = re.search(r'## .*?Certifications.*?\n(.*?)(?=##|$)', text, re.DOTALL | re.IGNORECASE)
        if certs_match:
            certs = certs_match.group(1).strip()

    # Extract Reference books
    books_match = re.search(r'## 📚 Best Books.*?\n(.*?)(?=##|$)', text, re.DOTALL | re.IGNORECASE)
    if books_match:
        books = books_match.group(1).strip()

    return months, certs, books


def render():
    st.markdown("""
    <div class="animate-in">
      <h2 style="margin-bottom:0.2rem; font-family:'Space Grotesk', sans-serif;">🗺️ Career Learning Path</h2>
      <p style="color:#64748B;margin-top:0;font-size:0.95rem;">
        Your custom 6-month master plan — interactive timelines, progress checklist toggles, and PDF exports.
      </p>
    </div>
    """, unsafe_allow_html=True)

    profile = memory.get_profile()

    if not memory.profile_complete():
        warning_box("Complete your profile first to generate a personalized roadmap.", "⚠️")
        return

    divider()

    # ── Target Career Selector ─────────────────────────────────────────────
    section_header("Roadmap Configuration", "⚙️")
    col1, col2 = st.columns([3, 1])
    with col1:
        target_career = st.text_input(
            "Target Career for Roadmap",
            value=memory.get("selected_career") or profile.get("career_goal", ""),
            placeholder="e.g. Frontend Engineer, Data Analyst, Cloud Solutions Architect",
        )
    with col2:
        st.markdown("<br/>", unsafe_allow_html=True)
        generate_btn = st.button(
            "🗺️ Build Roadmap",
            type="primary",
            use_container_width=True,
            key="gen_roadmap_btn",
        )

    # ── Synced Roadmap Cache check (Bugs Resolution) ───────────────────────
    cached_roadmap = memory.get("roadmap_output") or memory.get_agent_output("learning_roadmap")
    
    # Force synchronize state if one page has cache and the other doesn't
    if cached_roadmap and not memory.get("roadmap_output"):
        memory.set("roadmap_output", cached_roadmap)
    if cached_roadmap and not memory.get_agent_output("learning_roadmap"):
        memory.save_agent_output("learning_roadmap", cached_roadmap)

    if generate_btn:
        if not target_career.strip():
            st.error("⚠️ Please specify a target career role.")
        else:
            memory.set("selected_career", target_career)
            with st.spinner("🤖 Orchestrating 6-month learning curriculum..."):
                result = run_learning_roadmap(profile, target_career)
            memory.set("roadmap_output", result)
            memory.save_agent_output("learning_roadmap", result)
            cached_roadmap = result
            st.rerun()

    # ── Roadmap Display ────────────────────────────────────────────────────
    if cached_roadmap:
        divider()

        # Parse content dynamically
        months_data, certs_data, books_data = parse_roadmap_content(cached_roadmap)

        if months_data:
            section_header("Interactive Study Syllabus", "📅")
            
            # Progress checkboxes track
            if "roadmap_progress" not in st.session_state:
                st.session_state["roadmap_progress"] = {}
            
            # Render month accordions
            for month in months_data:
                num = month["number"]
                title = month["title"]
                content = month["content"]
                
                is_completed = st.session_state["roadmap_progress"].get(f"month_{num}", False)
                header_icon = "✓ " if is_completed else "⚙️ "
                header_style = "color:#10B981; font-weight:700;" if is_completed else "color:#0F172A; font-weight:700;"
                
                # Render accordion expander
                with st.expander(f"{header_icon} Month {num}: {title}", expanded=(num == 1 or not is_completed)):
                    st.markdown(content)
                    
                    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
                    check_val = st.checkbox(
                        f"I have completed the Month {num} syllabus",
                        value=is_completed,
                        key=f"check_month_{num}"
                    )
                    if check_val != is_completed:
                        st.session_state["roadmap_progress"][f"month_{num}"] = check_val
                        st.rerun()
            
            # Certs & books row
            if certs_data or books_data:
                divider()
                c_left, c_right = st.columns(2)
                
                with c_left:
                    if certs_data:
                        section_header("Suggested Certifications", "🏅")
                        st.markdown(f"""
                        <div class="np-card np-card-glow-purple" style="padding:1.5rem;">
                          <div style="font-size:0.9rem; line-height:1.6; color:#334155;">
                        """, unsafe_allow_html=True)
                        st.markdown(certs_data)
                        st.markdown("</div></div>", unsafe_allow_html=True)
                        
                with c_right:
                    if books_data:
                        section_header("Reference Material & Books", "📚")
                        st.markdown(f"""
                        <div class="np-card np-card-glow-blue" style="padding:1.5rem;">
                          <div style="font-size:0.9rem; line-height:1.6; color:#334155;">
                        """, unsafe_allow_html=True)
                        st.markdown(books_data)
                        st.markdown("</div></div>", unsafe_allow_html=True)

        else:
            # Fallback if markdown format couldn't be parsed
            st.markdown("""
            <div style="background:#F0FDF4; border-left:4px solid #10B981; padding:1.75rem; border-radius:12px;">
            """, unsafe_allow_html=True)
            st.markdown(cached_roadmap)
            st.markdown("</div>", unsafe_allow_html=True)

        divider()

        # ── Export Controls ────────────────────────────────────────────────
        section_header("Export & Sync Report", "📥")

        tab_m, tab_p = st.tabs(["📄 Export Pathway as MD", "📑 Generate Full Career PDF"])

        with tab_m:
            st.markdown("Download this roadmap pathway as a standalone Markdown file.")
            st.download_button(
                label="⬇️ Download Markdown Roadmap",
                data=cached_roadmap,
                file_name="career_roadmap.md",
                mime="text/markdown",
                use_container_width=True,
            )

        with tab_p:
            st.markdown(
                "Generate a premium, full career PDF report with student profile, SWOT analysis, "
                "roadmaps, recommended projects, resume feedback, and LinkedIn strategy."
            )
            render_export_button()

    else:
        st.markdown("""
        <div class="np-info-box animate-in" style="text-align:center; padding:2.5rem; justify-content:center; flex-direction:column;">
          <div style="font-size:3rem; margin-bottom:0.8rem;">🗺️</div>
          <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.2rem; color:#1E40AF; margin-bottom:0.3rem;">
            Your Learning Pathway Awaits
          </div>
          <div style="font-size:0.9rem; color:#3B82F6;">
            Enter your target career title above and click <strong>Build Roadmap</strong>.
          </div>
        </div>
        """, unsafe_allow_html=True)
