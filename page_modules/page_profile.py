# =============================================================================
# pages/page_profile.py  –  Student Profile entry form + profile card
# =============================================================================

import streamlit as st
from config.settings import DEGREES, BRANCHES, YEARS, INDUSTRIES
from ui.components import section_header, divider, skill_tags, profile_summary_card, success_box, info_box
import utils.memory as memory


def render():
    st.markdown("""
    <div class="animate-in">
      <h2 style="margin-bottom:0.2rem;">👤 My Student Profile</h2>
      <p style="color:#64748B;margin-top:0;">
        Fill in your details below. This information is used by all AI agents to personalise
        every recommendation for you.
      </p>
    </div>
    """, unsafe_allow_html=True)

    divider()

    profile = memory.get_profile()

    # ── Form ───────────────────────────────────────────────────────────────
    with st.form("profile_form", clear_on_submit=False):
        section_header("Personal Information", "📋")
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input(
                "Full Name *",
                value=profile.get("name", ""),
                placeholder="e.g. Priya Sharma",
            )
        with c2:
            degree = st.selectbox(
                "Degree *",
                options=DEGREES,
                index=DEGREES.index(profile.get("degree", DEGREES[0])) if profile.get("degree") in DEGREES else 0,
            )

        c3, c4 = st.columns(2)
        with c3:
            branch = st.selectbox(
                "Branch / Specialization *",
                options=BRANCHES,
                index=BRANCHES.index(profile.get("branch", BRANCHES[0])) if profile.get("branch") in BRANCHES else 0,
            )
        with c4:
            year = st.selectbox(
                "Year of Study *",
                options=YEARS,
                index=YEARS.index(profile.get("year", YEARS[0])) if profile.get("year") in YEARS else 0,
            )

        divider()
        section_header("Skills & Interests", "🛠️")

        skills = st.text_area(
            "Current Skills *",
            value=profile.get("skills", ""),
            placeholder="e.g. Python, Machine Learning, SQL, Data Visualisation, Pandas, Scikit-learn",
            height=90,
            help="List your technical and soft skills, separated by commas.",
        )
        interests = st.text_area(
            "Interests & Hobbies",
            value=profile.get("interests", ""),
            placeholder="e.g. Open-source contribution, Competitive programming, Reading, Teaching",
            height=80,
        )

        divider()
        section_header("Career Aspirations", "🎯")

        c5, c6 = st.columns(2)
        with c5:
            career_goal = st.text_input(
                "Career Goal *",
                value=profile.get("career_goal", ""),
                placeholder="e.g. Machine Learning Engineer at a product company",
            )
        with c6:
            industry = st.selectbox(
                "Preferred Industry *",
                options=INDUSTRIES,
                index=INDUSTRIES.index(profile.get("industry", INDUSTRIES[0])) if profile.get("industry") in INDUSTRIES else 0,
            )

        additional_info = st.text_area(
            "Anything else you'd like the AI to know?",
            value=profile.get("additional_info", ""),
            placeholder="e.g. I have done one internship in web development. I want to transition to data science. "
                        "I have 2 hours daily for learning.",
            height=90,
        )

        submitted = st.form_submit_button(
            "💾 Save Profile",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        # Validate required fields
        missing = []
        if not name.strip():     missing.append("Full Name")
        if not skills.strip():   missing.append("Current Skills")
        if not career_goal.strip(): missing.append("Career Goal")

        if missing:
            st.error(f"⚠️ Please fill in the required fields: **{', '.join(missing)}**")
        else:
            # Persist to session state
            memory.set("student_profile", {
                "name":            name.strip(),
                "degree":          degree,
                "branch":          branch,
                "year":            year,
                "skills":          skills.strip(),
                "interests":       interests.strip(),
                "career_goal":     career_goal.strip(),
                "industry":        industry,
                "additional_info": additional_info.strip(),
            })
            memory.set("onboarding_complete", True)
            # Clear cached agent outputs since profile changed
            memory.clear_agent_outputs()
            st.success("✅ Profile saved successfully! All AI agents have been refreshed.")
            st.balloons()

    divider()

    # ── Profile Preview ────────────────────────────────────────────────────
    updated_profile = memory.get_profile()
    if updated_profile and updated_profile.get("name"):
        section_header("Your Profile Card", "🪪")
        c_left, c_right = st.columns([1, 1])

        with c_left:
            profile_summary_card(updated_profile)

        with c_right:
            # Skills tags
            st.markdown("**🛠️ Your Skills**")
            skills_list = [s.strip() for s in updated_profile.get("skills", "").split(",") if s.strip()]
            skill_tags(skills_list, color="#1A56DB")

            if updated_profile.get("interests"):
                st.markdown("**💡 Interests**")
                interest_list = [i.strip() for i in updated_profile.get("interests", "").split(",") if i.strip()]
                skill_tags(interest_list, color="#7C3AED")

        divider()
        if memory.profile_complete():
            success_box(
                "Your profile is complete! Head to <strong>🤖 AI Agents</strong> to generate your "
                "full career analysis.",
                "🚀"
            )
        else:
            info_box(
                "Please fill all required fields (*) to unlock AI agent features.",
                "📝"
            )
    else:
        st.markdown("""
        <div class="np-info-box animate-in">
          📝 Fill out the form above and click <strong>Save Profile</strong> to see your profile card here.
        </div>
        """, unsafe_allow_html=True)
