# =============================================================================
# pages/page_agents.py  –  Multi-agent workflow with interactive visualization
# =============================================================================

import streamlit as st
import time
from datetime import datetime
import utils.memory as memory
from ui.components import (
    section_header, divider, score_card, warning_box, success_box,
    workflow_visualization, terminal_console, agent_card
)
from agents.profile_analyzer   import run_profile_analyzer
from agents.career_mentor       import run_career_mentor
from agents.learning_roadmap    import run_learning_roadmap
from agents.project_recommender import run_project_recommender
from agents.internship_readiness import run_internship_readiness
from agents.motivation_guidance  import run_motivation_guidance


# ─── Agent Configuration ──────────────────────────────────────────────────────
AGENTS = [
    {
        "key":   "profile_analyzer",
        "label": "Agent 1 · Profile Analyzer",
        "icon":  "🧠",
        "color": "#3B82F6",
        "desc":  "Analyses your background and generates a SWOT-style profile summary.",
        "fn":    run_profile_analyzer,
        "args":  lambda p: (p,),
    },
    {
        "key":   "career_mentor",
        "label": "Agent 2 · Career Mentor",
        "icon":  "🎯",
        "color": "#8B5CF6",
        "desc":  "Recommends top career paths with salary ranges and growth potential.",
        "fn":    run_career_mentor,
        "args":  lambda p: (p,),
    },
    {
        "key":   "learning_roadmap",
        "label": "Agent 3 · Learning Roadmap",
        "icon":  "🗺️",
        "color": "#10B981",
        "desc":  "Creates a detailed 6-month learning plan with courses and milestones.",
        "fn":    run_learning_roadmap,
        "args":  lambda p: (p, p.get("career_goal", "")),
    },
    {
        "key":   "project_recommender",
        "label": "Agent 4 · Project Recommender",
        "icon":  "🏗️",
        "color": "#F59E0B",
        "desc":  "Suggests beginner to advanced portfolio projects tailored to your goals.",
        "fn":    run_project_recommender,
        "args":  lambda p: (p, p.get("career_goal", "")),
    },
    {
        "key":   "internship_readiness",
        "label": "Agent 5 · Internship Readiness",
        "icon":  "💼",
        "color": "#EF4444",
        "desc":  "Scores your internship readiness and provides a 30-day action plan.",
        "fn":    run_internship_readiness,
        "args":  lambda p: (p,),
        "returns_tuple": True,
    },
    {
        "key":   "motivation_guidance",
        "label": "Agent 6 · Motivation & Guidance",
        "icon":  "🌟",
        "color": "#06B6D4",
        "desc":  "Delivers personalised motivation, competitive advantages, and next steps.",
        "fn":    run_motivation_guidance,
        "args":  lambda p: (p,),
    },
]


def render():
    st.markdown("""
    <div class="animate-in">
      <h2 style="margin-bottom:0.2rem; font-family:'Space Grotesk', sans-serif;">🤖 AI Agent Pipeline</h2>
      <p style="color:#64748B;margin-top:0;font-size:0.95rem;">
        An orchestrated swarm of six specialized AI agents analyzing your academic profile, skill gaps, and goals.
      </p>
    </div>
    """, unsafe_allow_html=True)

    profile = memory.get_profile()

    # Onboarding validations
    if not memory.profile_complete():
        warning_box(
            "Your profile is incomplete. Please go to <strong>👤 My Profile</strong> "
            "and fill in all required fields before running the agents.",
            "⚠️"
        )
        return

    divider()

    # ── Calculate Completed Keys ───────────────────────────────────────────
    cached = memory.get("agent_outputs", {})
    completed_keys = [
        a["key"] for a in AGENTS
        if memory.is_valid_ai_output(memory.get_agent_output_raw(a["key"]))
    ]
    
    # ── Interactive Pipeline Visualization ──────────────────────────────────
    active_agent = st.session_state.get("active_agent_key", "")
    workflow_visualization(active_agent, completed_keys)

    # ── Control Center ──────────────────────────────────────────────────────
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        run_all = st.button(
            "🚀 Run Full Agent Pipeline",
            type="primary",
            use_container_width=True,
            key="run_all_agents",
        )
    with col_b:
        if completed_keys:
            st.markdown(
                f'<div style="font-size:0.9rem;color:#10B981;font-weight:700;padding-top:0.6rem;text-align:center;">'
                f'✓ {len(completed_keys)}/6 Agents Active</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div style="font-size:0.9rem;color:#64748B;font-weight:700;padding-top:0.6rem;text-align:center;">'
                f'Pipeline Idle</div>',
                unsafe_allow_html=True,
            )
    with col_c:
        if st.button("🔄 Reset Agent Cache", use_container_width=True, key="clear_agents"):
            memory.clear_agent_outputs()
            st.session_state.pop("active_agent_key", None)
            st.session_state["pipeline_logs"] = [
                {"time": datetime.now().strftime("%H:%M:%S"), "type": "info", "msg": "Pipeline cache reset."}
            ]
            st.rerun()

    # ── Console Log Handler ────────────────────────────────────────────────
    if "pipeline_logs" not in st.session_state:
        st.session_state["pipeline_logs"] = [
            {"time": datetime.now().strftime("%H:%M:%S"), "type": "info", "msg": "System initialized. Ready to orchestrate."}
        ]

    # Console display area
    console_placeholder = st.empty()
    with console_placeholder:
        terminal_console(st.session_state["pipeline_logs"])

    # ── Automated Full Run Process ─────────────────────────────────────────
    if run_all:
        st.session_state["pipeline_logs"] = []
        def log_msg(msg_type, text):
            now = datetime.now().strftime("%H:%M:%S")
            st.session_state["pipeline_logs"].append({"time": now, "type": msg_type, "msg": text})
            with console_placeholder:
                terminal_console(st.session_state["pipeline_logs"])

        log_msg("info", f"Booting NayePankh Multi-Agent Pipeline for student: {profile.get('name')}")
        time.sleep(0.5)

        for agent in AGENTS:
            key   = agent["key"]
            icon  = agent["icon"]
            label = agent["label"]
            
            st.session_state["active_agent_key"] = key
            log_msg("warning", f"Activating {label}...")
            time.sleep(0.3)

            try:
                args = agent["args"](profile)
                result = agent["fn"](*args)

                if agent.get("returns_tuple"):
                    result, score = result
                    memory.set("internship_score", score)

                memory.save_agent_output(key, result)
                log_msg("success", f"{label} completed analysis successfully.")
            except Exception as e:
                err_msg = f"❌ Error running {key}: {str(e)}"
                memory.save_agent_output(key, err_msg)
                log_msg("red", f"{label} encountered an execution error.")
                
        st.session_state.pop("active_agent_key", None)
        log_msg("success", "Multi-Agent pipeline process completed. Full career intelligence cached.")
        st.rerun()

    divider()

    # ── Accordion Agent Output Detail ──────────────────────────────────────
    section_header("Pipeline Outputs & Insights", "📂")

    for agent in AGENTS:
        key   = agent["key"]
        icon  = agent["icon"]
        label = agent["label"]
        color = agent["color"]
        desc  = agent["desc"]

        cached_output = memory.get_agent_output_raw(key)

        with st.expander(f"{icon} {label}", expanded=(cached_output is not None)):
            st.markdown(
                f'<p style="font-size:0.88rem;color:#64748B;margin-bottom:1rem;line-height:1.5;">{desc}</p>',
                unsafe_allow_html=True,
            )

            # Individual execution
            btn_col, _ = st.columns([1, 3])
            with btn_col:
                individual_run = st.button(
                    f"▶ Run {icon}",
                    key=f"run_{key}",
                    use_container_width=True,
                )

            if individual_run:
                st.session_state["active_agent_key"] = key
                with st.spinner(f"Orchestrating {label}..."):
                    try:
                        args = agent["args"](profile)
                        result = agent["fn"](*args)
                        if agent.get("returns_tuple"):
                            result, score = result
                            memory.set("internship_score", score)
                        memory.save_agent_output(key, result)
                        cached_output = result
                    except Exception as e:
                        cached_output = f"❌ Error: {str(e)}"
                        memory.save_agent_output(key, cached_output)
                st.session_state.pop("active_agent_key", None)
                st.rerun()

            if cached_output:
                # Custom output display using our component
                agent_card(label, icon, cached_output, color)
                
                # Download widget
                st.download_button(
                    label="📋 Export this insight",
                    data=cached_output,
                    file_name=f"{key}_output.md",
                    mime="text/markdown",
                    key=f"dl_{key}",
                )
            else:
                st.markdown(
                    f'<div style="color:#94A3B8;font-size:0.85rem;text-align:center;background:rgba(226, 232, 240, 0.2);'
                    f'padding:1.5rem; border-radius: 10px; border:1px dashed var(--border);">'
                    f'Agent idle. Click <strong>▶ Run {icon}</strong> or trigger '
                    f'<strong>🚀 Run Full Agent Pipeline</strong> above.</div>',
                    unsafe_allow_html=True,
                )

    # ── Final Pipeline Completed Summary Section ───────────────────────────
    successful_agents = sum(
        1 for a in AGENTS
        if memory.is_valid_ai_output(memory.get_agent_output_raw(a["key"]))
    )
    if successful_agents >= 6:
        divider()
        section_header("🏆 Pipeline Intel Summary", "🏆")
        st.markdown("""
        <div class="np-card np-card-glow-green animate-in" style="background:linear-gradient(135deg,rgba(16, 185, 129, 0.05),white);">
          <p style="color:#065F46;font-size:0.95rem;line-height:1.7;font-weight:600;margin:0;">
            ✓ All 6 pipeline agents have completed execution and synthesized their intelligence report!
          </p>
        </div>
        """, unsafe_allow_html=True)

        intern_score = memory.get("internship_score", 0)
        resume_score = memory.get("resume_score", 0)
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            score_card("Internship Readiness", intern_score, "💼")
        with sc2:
            score_card("Resume Score", resume_score, "📄")
        with sc3:
            career_out = memory.get_agent_output("career_mentor") or ""
            n_careers  = career_out.count("###")
            score_card("Matched Career Paths", min(n_careers * 30, 100), "🎯")
        with sc4:
            score_card("Profile Integrity", 100 if memory.profile_complete() else 40, "🧠")

        success_box(
            "Your complete intelligence analysis report is synchronized! Go to <strong>🗺️ Career Roadmap</strong> "
            "to view your custom month-by-month checklist and download the full report.",
            "🎉"
        )
