# =============================================================================
# page_modules/page_about.py  –  About NayePankh Foundation
# =============================================================================

import streamlit as st
from ui.components import divider, section_header, feature_card
from ui.navigation import navigate_to
from config.settings import FOUNDATION_NAME, APP_NAME


def render():
    st.markdown(f"""
    <div class="np-hero animate-in" style="padding:2.5rem 2rem; margin-bottom:2rem;">
      <div style="position:relative;z-index:1;">
        <div style="font-size:0.8rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;opacity:0.85;margin-bottom:0.5rem;">
          🕊️ {FOUNDATION_NAME}
        </div>
        <div class="hero-title" style="font-size:2.4rem;">Empowering India's Next Generation</div>
        <div class="hero-sub" style="margin-top:0.75rem;">
          {FOUNDATION_NAME} bridges the opportunity gap for students — especially first-generation
          learners — through education, mentorship, and AI-powered career guidance.
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Who We Are ────────────────────────────────────────────────────────────
    section_header("Who We Are", "🕊️")
    st.markdown("""
    **NayePankh Foundation** is a student-centric nonprofit initiative focused on career readiness,
    skill development, and equitable access to professional guidance across India.

    We work with college students, recent graduates, and young professionals who lack access to
    structured mentorship, industry networks, or personalized career counselling — and we equip
    them with the tools, knowledge, and confidence to build meaningful careers.
    """)

    divider()

    # ── Mission & Vision ──────────────────────────────────────────────────────
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="np-card np-card-glow-blue animate-in">
          <div style="font-size:2rem;margin-bottom:0.75rem;">🎯</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:700;color:#0F172A;margin-bottom:0.5rem;">Our Mission</div>
          <div style="font-size:0.92rem;color:#475569;line-height:1.7;">
            Democratize world-class career counselling for underprivileged and first-generation
            college students. Every student deserves guidance that is personal, practical, and free
            from geographic or economic barriers.
          </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="np-card np-card-glow-purple animate-in">
          <div style="font-size:2rem;margin-bottom:0.75rem;">👁️</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:700;color:#0F172A;margin-bottom:0.5rem;">Our Vision</div>
          <div style="font-size:0.92rem;color:#475569;line-height:1.7;">
            A future where every student in India can discover their strengths, close skill gaps,
            access mentorship, and step confidently into careers that match their potential —
            regardless of where they come from.
          </div>
        </div>
        """, unsafe_allow_html=True)

    divider()

    # ── Core Pillars ──────────────────────────────────────────────────────────
    section_header("What We Do", "✨")
    c1, c2, c3 = st.columns(3)
    with c1:
        feature_card("🎓", "Education Initiatives",
                     "Workshops, bootcamps, and learning resources that help students build in-demand technical and professional skills.",
                     "#3B82F6")
    with c2:
        feature_card("💪", "Student Empowerment",
                     "Programs that build confidence, communication skills, and self-awareness — so students can advocate for themselves in interviews and workplaces.",
                     "#8B5CF6")
    with c3:
        feature_card("🎯", "Career Guidance",
                     "Structured career exploration, role matching, resume reviews, and internship readiness coaching tailored to each student's profile.",
                     "#10B981")

    c4, c5, c6 = st.columns(3)
    with c4:
        feature_card("🤝", "Mentorship Networks",
                     "Connecting students with alumni, industry professionals, and peer mentors who provide real-world perspective and accountability.",
                     "#F59E0B")
    with c5:
        feature_card("🌍", "Community Impact",
                     "Partnering with colleges, NGOs, and local communities to reach students who need support the most — in tier-2 and tier-3 cities across India.",
                     "#EF4444")
    with c6:
        feature_card("🤖", "AI-Powered Mentorship",
                     "This platform — built for NayePankh — uses advanced AI to deliver personalized SWOT analysis, learning roadmaps, and 24/7 career guidance at scale.",
                     "#06B6D4")

    divider()

    # ── AI Platform ───────────────────────────────────────────────────────────
    section_header("AI Career Mentor Platform", "🤖")
    st.markdown(f"""
    **{APP_NAME}** is NayePankh Foundation's flagship technology initiative. It brings together
    six specialized AI agents and integrated analysis tools to give every student a personal
    career intelligence report — something that would normally require hours of counsellor time.

    | Capability | What It Does |
    |---|---|
    | 🧠 Profile Analyzer | SWOT analysis of your academic background and skills |
    | 🎯 Career Mentor | Top career path recommendations with salary ranges |
    | 🗺️ Learning Roadmap | 6-month month-by-month study plan |
    | 🏗️ Project Recommender | Portfolio projects from beginner to advanced |
    | 💼 Internship Readiness | Scored readiness assessment + 30-day action plan |
    | 🌟 Motivation & Guidance | Personalized encouragement and next steps |
    | 📄 Resume Analyzer | ATS-compatible resume scoring and improvements |
    | 💼 LinkedIn Review | Profile optimization and headline rewrites |
    | 📊 Skill Gap Analysis | Priority-ranked skills to learn for your target role |
    | 💬 AI Chatbot | Context-aware career Q&A using your full profile |
    """)

    st.markdown("""
    <div class="np-success-box animate-in" style="margin-top:1rem;">
      <span>✅</span>
      <span><strong>Free for all students.</strong> No login required. Your data stays in your browser session.</span>
    </div>
    """, unsafe_allow_html=True)

    divider()

    # ── Impact ──────────────────────────────────────────────────────────────────
    section_header("Community Impact", "🌟")
    ic1, ic2, ic3, ic4 = st.columns(4)
    metrics = [
        ("🎓", "Students Reached", "1000+", "Across India"),
        ("🏆", "Placement Success", "200+", "Internships & jobs"),
        ("🏫", "Partner Institutions", "50+", "Colleges & NGOs"),
        ("🤖", "AI Sessions", "5000+", "Career analyses delivered"),
    ]
    for col, (icon, label, value, sub) in zip([ic1, ic2, ic3, ic4], metrics):
        with col:
            st.markdown(f"""
            <div class="np-metric animate-in">
              <div class="metric-icon-wrap">{icon}</div>
              <div class="metric-value">{value}</div>
              <div class="metric-label">{label}</div>
              <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # ── Get Involved ──────────────────────────────────────────────────────────
    section_header("Get Involved", "🤝")
    st.markdown("""
    Whether you are a **student** seeking guidance, a **professional** wanting to mentor,
    or an **organization** looking to partner — there is a place for you in the NayePankh community.
    """)

    g1, g2, g3 = st.columns(3)
    with g1:
        if st.button("👤 Start Your Profile", type="primary", use_container_width=True, key="about_go_profile"):
            navigate_to("profile")
            st.rerun()
    with g2:
        if st.button("🤖 Run AI Agents", use_container_width=True, key="about_go_agents"):
            navigate_to("agents")
            st.rerun()
    with g3:
        if st.button("💬 Try AI Chatbot", use_container_width=True, key="about_go_chat"):
            navigate_to("chatbot")
            st.rerun()

   st.markdown("""
### Connect with NayePankh Foundation

📸 **Instagram**  
https://www.instagram.com/nayepankhfoundation

💼 **LinkedIn**  
https://www.linkedin.com/company/nayepankh

🌐 **Website**  
https://www.nayepankh.com

▶️ **YouTube**  
https://youtube.com/@nayepankhfoundation

📘 **Facebook**  
https://facebook.com/nayepankhfoundation

---
Built for NayePankh Foundation · Developed by Mayank Mishra · © 2026
""")
