# =============================================================================
# pages/page_home.py  –  Landing / Home page
# =============================================================================

import streamlit as st
from ui.components import feature_card, divider, section_header, professional_footer
from ui.navigation import navigate_to
from utils.helpers import get_greeting
import utils.memory as memory


def render():
    profile = memory.get_profile()
    name    = profile.get("name", "")
    greeting = get_greeting()

    # ── Hero Banner ────────────────────────────────────────────────────────
    hero_name = f", {name}" if name else ""
    st.markdown(f"""
    <div class="np-hero animate-in">
      <div style="position:relative;z-index:1;">
        <div style="font-size:0.85rem;font-weight:600;opacity:0.8;
                    letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.5rem;">
          🕊️ NayePankh Career Mentor
        </div>
        <div class="hero-title">{greeting}{hero_name}! 👋<br>Your AI Career Mentor<br>is Ready.</div>
        <div class="hero-sub" style="margin-top:0.75rem;">
          Discover your ideal career path, close skill gaps, and build a standout
          portfolio — all powered by advanced AI technology.
        </div>
        <div style="margin-top:1.5rem;display:flex;gap:0.75rem;flex-wrap:wrap;">
          <span style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.3);
                       padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:600;">
            🤖 6 AI Agents
          </span>
          <span style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.3);
                       padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:600;">
            📄 Resume Analysis
          </span>
          <span style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.3);
                       padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:600;">
            🗺️ Career Roadmap
          </span>
          <span style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.3);
                       padding:6px 16px;border-radius:20px;font-size:0.82rem;font-weight:600;">
            💬 AI Chatbot
          </span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick Start ────────────────────────────────────────────────────────
    if not memory.profile_complete():
        st.markdown("""
        <div class="np-warning-box animate-in">
          ⚡ <strong>Get started:</strong> Fill in your student profile to unlock all AI features.
        </div>
        """, unsafe_allow_html=True)
        if st.button("👤 Go to My Profile", type="primary", key="home_go_profile"):
            navigate_to("profile")
            st.rerun()
    else:
        qa1, qa2, qa3 = st.columns(3)
        with qa1:
            if st.button("🤖 Run AI Agents", type="primary", use_container_width=True, key="home_go_agents"):
                navigate_to("agents")
                st.rerun()
        with qa2:
            if st.button("📈 View Dashboard", use_container_width=True, key="home_go_dash"):
                navigate_to("dashboard")
                st.rerun()
        with qa3:
            if st.button("💬 Open Chatbot", use_container_width=True, key="home_go_chat"):
                navigate_to("chatbot")
                st.rerun()

    divider()

    # ── Feature Grid ───────────────────────────────────────────────────────
    section_header("What Can NayePankh Mentor Do For You?", "✨")

    c1, c2, c3 = st.columns(3)
    with c1:
        feature_card("🧠", "Profile Analysis",
                     "AI-powered SWOT analysis of your academic background, skills, and interests.",
                     "#1A56DB")
    with c2:
        feature_card("🎯", "Career Matching",
                     "Discover the top career paths that align with your profile, with salary ranges and growth potential.",
                     "#7C3AED")
    with c3:
        feature_card("🗺️", "6-Month Roadmap",
                     "A personalised month-by-month learning plan with recommended courses and milestones.",
                     "#059669")

    c4, c5, c6 = st.columns(3)
    with c4:
        feature_card("🏗️", "Project Ideas",
                     "Beginner to advanced project recommendations that build your portfolio step by step.",
                     "#D97706")
    with c5:
        feature_card("💼", "Internship Readiness",
                     "Get scored on your readiness and receive a 30-day action plan to land your first internship.",
                     "#DC2626")
    with c6:
        feature_card("📄", "Resume & LinkedIn",
                     "Upload your resume for a score out of 100 and AI-driven improvement suggestions.",
                     "#0891B2")

    divider()

    # ── How It Works ───────────────────────────────────────────────────────
    section_header("How It Works", "⚙️")
    steps = [
        ("1", "Fill Your Profile", "Tell us your degree, skills, interests, and career goal."),
        ("2", "Run AI Agents",     "Six specialised agents analyse your profile and generate insights."),
        ("3", "Get Recommendations", "Receive personalised career paths, roadmaps, and project ideas."),
        ("4", "Track Progress",    "Monitor your goals and chat with your AI mentor for guidance."),
    ]
    cols = st.columns(4)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="np-card animate-in" style="text-align:center;padding:1.25rem 1rem;">
              <div style="width:40px;height:40px;border-radius:50%;
                          background:linear-gradient(135deg,#1A56DB,#7C3AED);
                          color:white;font-size:1.1rem;font-weight:800;
                          display:flex;align-items:center;justify-content:center;
                          margin:0 auto 0.75rem;">
                {num}
              </div>
              <div style="font-weight:700;font-size:0.95rem;color:#1E293B;margin-bottom:0.4rem;">{title}</div>
              <div style="font-size:0.82rem;color:#64748B;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # ── Agent Cards ────────────────────────────────────────────────────────
    section_header("Meet Your AI Agents", "🤖")
    agents = [
        ("🧠", "Profile Analyzer",     "SWOT analysis · Strength mapping · Opportunity identification", "#1A56DB"),
        ("🎯", "Career Mentor",         "Career path recommendations · Salary insights · Role matching",   "#7C3AED"),
        ("🗺️", "Learning Roadmap",      "6-month plan · Course suggestions · Monthly milestones",         "#059669"),
        ("🏗️", "Project Recommender",   "3-tier project ideas · Tech stacks · Portfolio outcomes",        "#D97706"),
        ("💼", "Internship Readiness",  "Readiness score · Portfolio tips · 30-day action plan",          "#DC2626"),
        ("🌟", "Motivation & Guidance", "Personalised advice · Next steps · Inspirational coaching",      "#0891B2"),
    ]
    for i in range(0, len(agents), 3):
        cols = st.columns(3)
        for col, (icon, name_a, desc, color) in zip(cols, agents[i:i+3]):
            with col:
                st.markdown(f"""
                <div class="np-card animate-in" style="border-top:3px solid {color};">
                  <div style="font-size:1.8rem;margin-bottom:0.5rem;">{icon}</div>
                  <div style="font-weight:700;color:#1E293B;font-size:0.95rem;margin-bottom:0.4rem;">{name_a}</div>
                  <div style="font-size:0.8rem;color:#64748B;line-height:1.6;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

    divider()

    # ── NayePankh About ────────────────────────────────────────────────────
    st.markdown("""
    <div class="np-card animate-in" style="background:linear-gradient(135deg,#EFF6FF,#F5F3FF);
                                            border:1px solid #C7D2FE;">
      <div style="display:flex;align-items:flex-start;gap:1rem;">
        <div style="font-size:2.5rem;flex-shrink:0;">🕊️</div>
        <div>
          <div style="font-family:'Poppins',sans-serif;font-size:1.1rem;font-weight:700;
                      color:#1E293B;margin-bottom:0.4rem;">About NayePankh Foundation</div>
          <div style="font-size:0.88rem;color:#475569;line-height:1.7;">
            NayePankh Foundation is a non-profit organisation dedicated to empowering underprivileged 
            students across India by providing career guidance, skill development resources, and 
            mentorship opportunities. This AI-powered Career Mentor tool is part of our mission 
            to make world-class career counselling accessible to every student — regardless of 
            their background or location.
          </div>
          <div style="margin-top:0.8rem;">
            <span class="np-badge np-badge-blue">🎓 Education</span>
            <span class="np-badge np-badge-purple">💡 Skill Development</span>
            <span class="np-badge np-badge-green">🚀 Career Growth</span>
            <span class="np-badge np-badge-amber">🤝 Community</span>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Professional Footer ────────────────────────────────────────────────────
    professional_footer()
