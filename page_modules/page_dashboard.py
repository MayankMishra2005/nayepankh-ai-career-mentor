# =============================================================================
# pages/page_dashboard.py  –  Summary Dashboard with circular metrics & cards
# =============================================================================

import streamlit as st
import utils.memory as memory
from ui.components import (
    section_header, divider, score_card, premium_metric_card,
    radial_score_bar, profile_summary_card, skill_tags, warning_box, info_box
)
from ui.navigation import navigate_to
from utils.helpers import parse_skills_list, score_to_color, score_to_label, score_to_emoji


def _completion_pct() -> int:
    """Calculate overall platform completion percentage."""
    checks = [
        memory.profile_complete(),
        memory.is_valid_ai_output(memory.get_agent_output_raw("profile_analyzer")),
        memory.is_valid_ai_output(memory.get_agent_output_raw("career_mentor")),
        memory.is_valid_ai_output(memory.get_agent_output_raw("learning_roadmap")),
        memory.is_valid_ai_output(memory.get_agent_output_raw("project_recommender")),
        memory.is_valid_ai_output(memory.get_agent_output_raw("internship_readiness")),
        memory.is_valid_ai_output(memory.get_agent_output_raw("motivation_guidance")),
        memory.is_valid_ai_output(memory.get("resume_analysis")),
        memory.is_valid_ai_output(memory.get("linkedin_analysis")),
        memory.is_valid_ai_output(memory.get("skill_gap_analysis")),
    ]
    return int(sum(checks) / len(checks) * 100)


def render():
    profile = memory.get_profile()

    # ── Header ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="animate-in">
      <h2 style="margin-bottom:0.2rem; font-family:'Space Grotesk', sans-serif;">📈 Career Intelligence Command Center</h2>
      <p style="color:#64748B;margin-top:0;font-size:0.95rem;">
        Your synchronized career readiness center — circular score rings, metrics, and agent logs at a glance.
      </p>
    </div>
    """, unsafe_allow_html=True)

    if not memory.profile_complete():
        warning_box(
            "Your profile is incomplete. Visit <strong>👤 My Profile</strong> to unlock all dashboard analytics.",
            "⚠️"
        )

    divider()

    # ── Platform Progress Banner ──────────────────────────────────────────
    completion = _completion_pct()
    comp_color = score_to_color(completion)
    st.markdown(f"""
    <div class="np-card animate-in" style="border-left: 5px solid {comp_color};
         background: linear-gradient(135deg, {'rgba(16,185,129,0.04)' if completion>=70 else 'rgba(245,158,11,0.04)'}, white);">
      <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1.5rem;">
        <div>
          <div style="font-size:0.75rem; font-weight:700; color:{comp_color};
                      text-transform:uppercase; letter-spacing:0.08em;">Overall Pipeline Progress</div>
          <div style="font-family:'Space Grotesk', sans-serif; font-size:1.8rem; font-weight:700; color:#0F172A; margin:0.3rem 0;">
            {completion}% Analytical Complete {score_to_emoji(completion)}
          </div>
          <div style="font-size:0.88rem; color:#64748B;">Rating: <strong>{score_to_label(completion)}</strong> · Complete all modules to unlock full PDF report capability.</div>
        </div>
        <div style="min-width:300px; flex:1; max-width: 500px;">
          <div class="np-progress-wrap" style="height:12px;">
            <div class="np-progress-fill"
                 style="width:{completion}%; background:linear-gradient(90deg, {comp_color}, {comp_color}AA);">
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Scores Row (Circular Progress Rings) ──────────────────────────────
    section_header("Circular Metric Indicators", "🔮")
    
    resume_score  = memory.get("resume_score", 0)
    intern_score  = memory.get("internship_score", 0)
    profile_score = 100 if memory.profile_complete() else 40
    
    # Career paths count logic
    career_out    = memory.get_agent_output("career_mentor") or ""
    n_careers     = min(career_out.count("###") * 30, 100) if career_out else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: radial_score_bar("Resume Score",         resume_score,  "📄")
    with c2: radial_score_bar("Internship Readiness", intern_score,  "💼")
    with c3: radial_score_bar("Profile Integrity",    profile_score, "👤")
    with c4: radial_score_bar("Career Match Index",    n_careers,     "🎯")

    divider()

    # ── Profile + Goals Overview ──────────────────────────────────────────
    col_l, col_r = st.columns([1, 1])
    
    with col_l:
        section_header("Student Profile Card", "🪪")
        if profile:
            profile_summary_card(profile)
        else:
            info_box("Complete your profile to see summary card.")
            
    with col_r:
        section_header("Skills & Targets", "🛠️")
        if profile.get("skills"):
            st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#0F172A; margin-bottom:0.4rem;'>🛠️ Current Skill Tags</p>", unsafe_allow_html=True)
            skill_tags(parse_skills_list(profile.get("skills", "")), color="#3B82F6")
            
        if profile.get("career_goal"):
            st.markdown(f"""
            <div style="margin-top:1.25rem; padding:1rem 1.25rem; background:rgba(59, 130, 246, 0.05);
                        border-radius:12px; border:1px solid rgba(59, 130, 246, 0.15); display:flex; flex-direction:column; gap:2px;">
              <span style="font-size:0.75rem; font-weight:700; color:#3B82F6;
                          text-transform:uppercase; letter-spacing:0.06em;">Target Career Goal</span>
              <span style="font-family:'Space Grotesk', sans-serif; font-size:1.05rem; font-weight:700; color:#0F172A; margin-top:2px;">
                {profile.get('career_goal')}
              </span>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # ── Agent Status Grid ──────────────────────────────────────────────────
    section_header("Multi-Agent Swarm Status", "🤖")
    agent_info = [
        ("profile_analyzer",    "🧠", "Profile Analyzer",     "#3B82F6"),
        ("career_mentor",       "🎯", "Career Mentor",         "#8B5CF6"),
        ("learning_roadmap",    "🗺️", "Learning Roadmap",     "#10B981"),
        ("project_recommender", "🏗️", "Project Recommender",  "#F59E0B"),
        ("internship_readiness","💼", "Internship Readiness",  "#EF4444"),
        ("motivation_guidance", "🌟", "Motivation & Guidance", "#06B6D4"),
    ]

    cols = st.columns(3)
    for i, (key, icon, label, color) in enumerate(agent_info):
        output  = memory.get_agent_output_raw(key)
        done    = memory.is_valid_ai_output(output)
        status  = "✓ Completed & Cached" if done else "⬜ Not Executed"
        s_color = "#10B981" if done else "#64748B"
        bg      = "rgba(16, 185, 129, 0.04)" if done else "rgba(255, 255, 255, 0.6)"
        border  = "rgba(16, 185, 129, 0.2)" if done else "var(--border)"

        with cols[i % 3]:
            st.markdown(f"""
            <div class="np-card animate-in"
                 style="background:{bg}; border-color:{border}; border-top:4px solid {color if done else '#E2E8F0'}; padding: 1.25rem;">
              <div style="display:flex; align-items:center; gap:0.75rem;">
                <span style="font-size:1.8rem; padding:0.4rem; background:{color}0F; border-radius:10px;">{icon}</span>
                <div>
                  <div style="font-family:'Space Grotesk', sans-serif; font-size:0.95rem; font-weight:700; color:#0F172A;">{label}</div>
                  <div style="font-size:0.78rem; font-weight:700; color:{s_color}; margin-top:2px;">{status}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # ── Module Status ──────────────────────────────────────────────────────
    section_header("System Integration Modules", "📦")
    modules = [
        ("resume_analysis",   "📄", "Resume Review",  "#3B82F6"),
        ("linkedin_analysis", "💼", "LinkedIn Audit",  "#8B5CF6"),
        ("skill_gap_analysis","📊", "Skill Gap Map",  "#F59E0B"),
        ("roadmap_output",    "🗺️", "Checklist Sync", "#10B981"),
    ]
    mcols = st.columns(4)
    for col, (key, icon, label, color) in zip(mcols, modules):
        val    = memory.get(key)
        done   = memory.is_valid_ai_output(val)
        status = "COMPLETE" if done else "PENDING"
        text_col  = "#10B981" if done else "#64748B"
        with col:
            premium_metric_card(label, icon, status, icon, text_col)

    divider()

    # ── Recommended Next Steps ─────────────────────────────────────────────
    section_header("AI Action Strategy Tracker", "🎯")
    steps = []
    if not memory.profile_complete():
        steps.append(("👤", "Configure student background credentials", "profile"))
    if not memory.is_valid_ai_output(memory.get_agent_output_raw("profile_analyzer")):
        steps.append(("🤖", "Execute Multi-Agent pipeline orchestration", "agents"))
    if not memory.is_valid_ai_output(memory.get("resume_analysis")):
        steps.append(("📄", "Upload resume and trigger ATS score parser", "resume"))
    if not memory.is_valid_ai_output(memory.get("skill_gap_analysis")):
        steps.append(("📊", "Compare technical skill sets to target goal", "skillgap"))
    if not memory.is_valid_ai_output(memory.get("roadmap_output")):
        steps.append(("🗺️", "Generate 6-month visual learning syllabus", "roadmap"))
    if len(memory.get_chat_history()) == 0:
        steps.append(("💬", "Discuss roadmap milestones with Career Mentor AI", "chatbot"))

    if steps:
        for i, (icon, action, page_key) in enumerate(steps[:4]):
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:0.8rem; padding:0.9rem 1.25rem;
                            background:white; border-radius:10px; margin-bottom:0.5rem; border: 1px solid var(--border);" class="animate-in">
                  <span style="font-size:1.4rem;">{icon}</span>
                  <div>
                    <div style="font-weight:600; font-size:0.92rem; color:#0F172A;">{action}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with col_b:
                if st.button("Go →", key=f"nav_step_{i}", use_container_width=True):
                    navigate_to(page_key)
                    st.rerun()
    else:
        st.markdown("""
        <div class="np-success-box animate-in">
          🏆 <strong>All modules completed successfully!</strong> Your portfolio report is ready. 
          Download your comprehensive career intelligence PDF from the <strong>🗺️ Career Roadmap</strong> page.
        </div>
        """, unsafe_allow_html=True)
