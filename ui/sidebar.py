# =============================================================================
# ui/sidebar.py  –  Sidebar navigation + memory controls
# =============================================================================

import streamlit as st
from config.settings import PAGES, APP_VERSION
import utils.memory as memory
from utils.llm_client import get_api_key, verify_api_connection
from ui.navigation import apply_nav_override


def render_sidebar() -> str:
    """
    Render the full sidebar.
    Returns the key of the currently selected page (e.g. 'home').
    """
    with st.sidebar:
        # ── Logo / Branding ────────────────────────────────────────────────
        st.markdown("""
        <div style="padding:1.2rem 0.5rem 0.8rem;">
          <div class="np-logo-text">🕊️ NayePankh</div>
          <div class="np-logo-sub">Career Mentor AI</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:0 0 1rem;"/>',
            unsafe_allow_html=True,
        )

        # ── Navigation ─────────────────────────────────────────────────────
        st.markdown(
            '<p style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;'
            'color:#94A3B8;text-transform:uppercase;margin-bottom:0.3rem;">Navigation</p>',
            unsafe_allow_html=True,
        )

        page_labels = list(PAGES.keys())
        apply_nav_override()
        selected_label = st.radio(
            label="nav",
            options=page_labels,
            label_visibility="collapsed",
            key="nav_radio",
        )
        selected_page = PAGES[selected_label]

        st.markdown(
            '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:1rem 0;"/>',
            unsafe_allow_html=True,
        )

        # ── Profile Status ─────────────────────────────────────────────────
        profile = memory.get_profile()
        if memory.profile_complete():
            name = profile.get("name", "Student")
            st.markdown(f"""
            <div style="background:rgba(5,150,105,0.15);border:1px solid rgba(52,211,153,0.3);
                        border-radius:10px;padding:0.7rem 0.9rem;margin-bottom:0.8rem;">
              <div style="font-size:0.72rem;color:#34D399;font-weight:700;text-transform:uppercase;">
                ✓ Profile Active
              </div>
              <div style="font-size:0.9rem;font-weight:700;color:#E2E8F0;margin-top:2px;">
                {name}
              </div>
              <div style="font-size:0.75rem;color:#94A3B8;">
                {profile.get('branch','')}, {profile.get('year','')}
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(217,119,6,0.15);border:1px solid rgba(251,191,36,0.3);
                        border-radius:10px;padding:0.7rem 0.9rem;margin-bottom:0.8rem;">
              <div style="font-size:0.72rem;color:#FCD34D;font-weight:700;">⚠️ Profile Incomplete</div>
              <div style="font-size:0.78rem;color:#94A3B8;margin-top:2px;">
                Fill your profile to unlock all AI features.
              </div>
            </div>
            """, unsafe_allow_html=True)

        # ── API Status (verified once per session) ─────────────────────────
        if "api_verified" not in st.session_state:
            st.session_state["api_verified"] = None

        if get_api_key():
            if st.session_state["api_verified"] is None:
                st.session_state["api_verified"] = verify_api_connection()
            ok, api_msg = st.session_state["api_verified"]
            if ok:
                st.markdown(f"""
                <div style="background:rgba(5,150,105,0.12);border:1px solid rgba(52,211,153,0.3);
                            border-radius:10px;padding:0.55rem 0.8rem;margin-bottom:0.8rem;">
                  <div style="font-size:0.72rem;color:#34D399;font-weight:700;">✓ {api_msg}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background:rgba(245,158,11,0.12);border:1px solid rgba(251,191,36,0.3);
                            border-radius:10px;padding:0.55rem 0.8rem;margin-bottom:0.8rem;">
                  <div style="font-size:0.72rem;color:#FCD34D;font-weight:700;">⚠️ {api_msg}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(239,68,68,0.12);border:1px solid rgba(248,113,113,0.3);
                        border-radius:10px;padding:0.55rem 0.8rem;margin-bottom:0.8rem;">
              <div style="font-size:0.72rem;color:#FCA5A5;font-weight:700;">🔑 Groq API Key Missing</div>
              <div style="font-size:0.72rem;color:#94A3B8;margin-top:2px;">Add GROQ_API_KEY to .env</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Memory Controls ────────────────────────────────────────────────
        st.markdown(
            '<p style="font-size:0.7rem;font-weight:700;letter-spacing:0.1em;'
            'color:#94A3B8;text-transform:uppercase;margin-bottom:0.4rem;">🧠 Session</p>',
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑 Clear Chat", use_container_width=True, key="clear_chat_btn"):
                memory.clear_chat_history()
                st.success("Chat cleared!")
        with col2:
            if st.button("♻️ Reset", use_container_width=True, key="reset_all_btn"):
                memory.clear_all_memory()
                st.session_state.pop("api_verified", None)
                st.success("Session reset!")
                st.rerun()

        # ── Footer ─────────────────────────────────────────────────────────
        st.markdown(
            f'<div style="margin-top:auto;padding-top:2rem;font-size:0.65rem;'
            f'color:#64748B;text-align:center;line-height:1.4;">'
            f'NayePankh Career Mentor<br>'
            f'v{APP_VERSION}</div>',
            unsafe_allow_html=True,
        )

    return selected_page
