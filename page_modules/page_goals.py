# =============================================================================
# pages/page_goals.py  –  Goal Tracker + Learning Checklist + Certifications
# =============================================================================

import streamlit as st
import utils.memory as memory
from ui.components import section_header, divider, warning_box, success_box, step_badge
from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt


# ─── Recommended Certifications by Domain ─────────────────────────────────────
CERT_DATABASE = {
    "Data Science & AI/ML": [
        ("Google Data Analytics Certificate",      "Coursera · ~6 months",  "Beginner"),
        ("IBM Data Science Professional",           "Coursera · ~10 months", "Beginner"),
        ("TensorFlow Developer Certificate",        "Google · Exam",         "Intermediate"),
        ("AWS Certified Machine Learning",          "AWS · Exam",            "Advanced"),
        ("Deep Learning Specialisation (deeplearning.ai)", "Coursera · ~4 months", "Intermediate"),
    ],
    "Technology / Software": [
        ("Meta Front-End Developer Certificate",    "Coursera · ~7 months",  "Beginner"),
        ("AWS Certified Developer – Associate",     "AWS · Exam",            "Intermediate"),
        ("Google Associate Cloud Engineer",         "Google · Exam",         "Intermediate"),
        ("Certified Kubernetes Administrator",      "CNCF · Exam",           "Advanced"),
        ("MongoDB Developer Certificate",           "MongoDB · Exam",        "Intermediate"),
    ],
    "Finance & FinTech": [
        ("CFA Level 1",                             "CFA Institute · Exam",  "Advanced"),
        ("NISM Series Certifications",              "NISM · Exam",           "Beginner"),
        ("Financial Modelling & Valuation Analyst", "CFI · Online",          "Intermediate"),
        ("Bloomberg Market Concepts",               "Bloomberg · Online",    "Beginner"),
    ],
    "Product Management": [
        ("Google Project Management Certificate",   "Coursera · ~6 months",  "Beginner"),
        ("Certified Scrum Product Owner (CSPO)",    "Scrum Alliance · 2 days","Intermediate"),
        ("Product School PM Certificate",           "ProductSchool · Online","Intermediate"),
    ],
}

DEFAULT_CERTS = [
    ("Python for Everybody",                    "Coursera (U-Michigan) · 8 weeks", "Beginner"),
    ("Git & GitHub Bootcamp",                   "Udemy · Self-paced",              "Beginner"),
    ("Communication Skills Certificate",        "Coursera · 4 weeks",              "Beginner"),
    ("SQL for Data Analysis",                   "Mode Analytics · Free",           "Beginner"),
    ("Introduction to Cloud Computing",         "IBM via Coursera · 5 weeks",      "Beginner"),
]

CHECKLIST_ITEMS = [
    "Update LinkedIn profile",
    "Write a strong resume summary",
    "Build a GitHub portfolio",
    "Complete 1 beginner project",
    "Apply for 5 internships",
    "Attend a tech event / hackathon",
    "Get 1 certification",
    "Complete online course this month",
    "Practice LeetCode (Easy problems)",
    "Research target companies",
    "Set up professional email",
    "Network with 3 industry professionals",
]


def _get_ai_tips(profile: dict) -> str:
    """Generate AI internship prep tips."""
    profile_text = format_profile_for_prompt(profile)
    prompt = f"""
You are a career coach at NayePankh Foundation.
Give 8 specific, actionable internship preparation tips for this student.
Format as a numbered list with bold headers and 1-line descriptions.
Keep it practical and specific to their profile.

Student Profile:
{profile_text}
"""
    return call_llm(prompt)


def render():
    st.markdown("""
    <div class="animate-in">
      <h2 style="margin-bottom:0.2rem;">🎯 Goal Tracker & Learning Hub</h2>
      <p style="color:#64748B;margin-top:0;">
        Track your career goals, monitor your learning checklist, discover recommended
        certifications, and get personalised internship preparation tips.
      </p>
    </div>
    """, unsafe_allow_html=True)

    profile  = memory.get_profile()
    industry = profile.get("industry", "Technology / Software")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Goal Tracker",
        "✅ Learning Checklist",
        "🏅 Certifications",
        "💡 Internship Tips",
    ])

    # ─────────────────────────────────────────────────────────────────────
    # Tab 1 – Goal Tracker
    # ─────────────────────────────────────────────────────────────────────
    with tab1:
        divider()
        section_header("Add a New Goal", "➕")

        col1, col2 = st.columns([4, 1])
        with col1:
            new_goal = st.text_input(
                "Goal",
                placeholder="e.g. Complete Python course by July · Apply to 10 internships · Build a portfolio project",
                label_visibility="collapsed",
                key="new_goal_input",
            )
        with col2:
            if st.button("Add Goal", type="primary", use_container_width=True, key="add_goal_btn"):
                if new_goal.strip():
                    memory.add_goal(new_goal.strip())
                    st.success("✅ Goal added!")
                    st.rerun()
                else:
                    st.error("Please enter a goal.")

        divider()
        section_header("Your Goals", "📋")

        goals = memory.get("goals", [])
        if not goals:
            st.markdown("""
            <div class="np-info-box" style="text-align:center;padding:2rem;">
              <div style="font-size:1.5rem;">🎯</div>
              <div style="font-weight:600;margin-top:0.4rem;">No goals yet</div>
              <div style="font-size:0.85rem;margin-top:0.2rem;">Add your first career goal above!</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            done_count  = sum(1 for g in goals if g["done"])
            total_count = len(goals)
            pct         = int(done_count / total_count * 100) if total_count else 0

            st.markdown(f"""
            <div style="display:flex;align-items:center;justify-content:space-between;
                        margin-bottom:0.8rem;">
              <span style="font-size:0.9rem;font-weight:600;color:#1E293B;">
                {done_count}/{total_count} goals completed
              </span>
              <span style="font-size:0.85rem;font-weight:700;color:#059669;">{pct}%</span>
            </div>
            <div class="np-progress-wrap" style="height:8px;margin-bottom:1.2rem;">
              <div class="np-progress-fill"
                   style="width:{pct}%;background:linear-gradient(90deg,#1A56DB,#059669);">
              </div>
            </div>
            """, unsafe_allow_html=True)

            for i, goal in enumerate(goals):
                gcol1, gcol2, gcol3 = st.columns([0.5, 5, 0.5])
                with gcol1:
                    if st.checkbox(
                        "", value=goal["done"],
                        key=f"goal_check_{i}",
                        label_visibility="collapsed"
                    ):
                        if not goal["done"]:
                            memory.toggle_goal(i)
                            st.rerun()
                    else:
                        if goal["done"]:
                            memory.toggle_goal(i)
                            st.rerun()

                with gcol2:
                    style = "text-decoration:line-through;color:#94A3B8;" if goal["done"] else "color:#1E293B;font-weight:500;"
                    st.markdown(
                        f'<div style="{style}font-size:0.9rem;padding-top:0.4rem;">'
                        f'{"✅ " if goal["done"] else ""}{goal["text"]}'
                        f'<span style="font-size:0.72rem;color:#94A3B8;margin-left:0.5rem;">'
                        f'Added {goal.get("created","")}</span></div>',
                        unsafe_allow_html=True,
                    )
                with gcol3:
                    if st.button("🗑", key=f"del_goal_{i}", help="Delete goal"):
                        memory.remove_goal(i)
                        st.rerun()

    # ─────────────────────────────────────────────────────────────────────
    # Tab 2 – Learning Checklist
    # ─────────────────────────────────────────────────────────────────────
    with tab2:
        divider()
        section_header("Internship Readiness Checklist", "✅")

        checklist = memory.get("checklist", {})
        done_items = sum(1 for v in checklist.values() if v)

        st.markdown(f"""
        <div style="font-size:0.88rem;color:#64748B;margin-bottom:0.8rem;">
          {done_items}/{len(CHECKLIST_ITEMS)} items completed
        </div>
        <div class="np-progress-wrap" style="margin-bottom:1.2rem;">
          <div class="np-progress-fill"
               style="width:{int(done_items/len(CHECKLIST_ITEMS)*100)}%;
                      background:linear-gradient(90deg,#059669,#34D399);">
          </div>
        </div>
        """, unsafe_allow_html=True)

        for item in CHECKLIST_ITEMS:
            checked = checklist.get(item, False)
            new_val = st.checkbox(item, value=checked, key=f"cl_{item}")
            if new_val != checked:
                checklist[item] = new_val
                memory.set("checklist", checklist)
                st.rerun()

        if done_items == len(CHECKLIST_ITEMS):
            success_box(
                "🎉 Checklist complete! You're ready to apply for internships. Good luck!",
                "🏆"
            )

    # ─────────────────────────────────────────────────────────────────────
    # Tab 3 – Certifications
    # ─────────────────────────────────────────────────────────────────────
    with tab3:
        divider()
        section_header(f"Recommended Certifications — {industry}", "🏅")

        certs = CERT_DATABASE.get(industry, DEFAULT_CERTS)

        badge_colors = {"Beginner": "#059669", "Intermediate": "#D97706", "Advanced": "#DC2626"}

        for cert_name, platform, level in certs:
            color = badge_colors.get(level, "#64748B")
            st.markdown(f"""
            <div class="np-card animate-in" style="padding:1rem 1.25rem;">
              <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
                <div>
                  <div style="font-weight:700;font-size:0.95rem;color:#1E293B;">🏅 {cert_name}</div>
                  <div style="font-size:0.8rem;color:#64748B;margin-top:2px;">📍 {platform}</div>
                </div>
                <span class="np-badge" style="background:{color}15;color:{color};border:1px solid {color}40;">
                  {level}
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)

        divider()
        section_header("Universal Starter Certifications", "🌐")
        for cert_name, platform, level in DEFAULT_CERTS:
            color = badge_colors.get(level, "#64748B")
            st.markdown(f"""
            <div class="np-card animate-in" style="padding:0.9rem 1.25rem;">
              <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
                <div>
                  <div style="font-weight:700;font-size:0.9rem;color:#1E293B;">🎓 {cert_name}</div>
                  <div style="font-size:0.78rem;color:#64748B;">📍 {platform}</div>
                </div>
                <span class="np-badge" style="background:{color}15;color:{color};border:1px solid {color}40;">
                  {level}
                </span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────
    # Tab 4 – Internship Tips
    # ─────────────────────────────────────────────────────────────────────
    with tab4:
        divider()
        section_header("AI Internship Preparation Tips", "💡")

        cached_tips = memory.get("agent_outputs", {}).get("internship_tips", {})
        cached_content = cached_tips.get("content", "") if cached_tips else ""

        if not cached_content:
            if st.button("🤖 Generate My Internship Tips", type="primary", use_container_width=True, key="gen_tips"):
                with st.spinner("Generating personalised internship tips..."):
                    tips = _get_ai_tips(profile)
                memory.save_agent_output("internship_tips", tips)
                cached_content = tips
                st.rerun()

        if cached_content:
            st.markdown("""
            <div style="background:#F5F3FF;border:1px solid #DDD6FE;border-left:4px solid #7C3AED;
                        border-radius:12px;padding:1.5rem;">
            """, unsafe_allow_html=True)
            st.markdown(cached_content)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="np-info-box" style="text-align:center;padding:2rem;">
              <div style="font-size:1.5rem;">💡</div>
              <div style="font-weight:600;margin-top:0.4rem;">Click above to generate your personalised tips</div>
            </div>
            """, unsafe_allow_html=True)
