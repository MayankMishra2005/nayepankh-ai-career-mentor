# =============================================================================
# app.py  –  NayePankh Career Mentor AI Agent
# Main Streamlit entry point: page routing, layout, CSS injection.
# =============================================================================

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ── Streamlit page config (MUST be first st call) ─────────────────────────────
st.set_page_config(
    page_title="NayePankh Career Mentor",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Internal imports (after page config) ──────────────────────────────────────
import utils.memory as memory
from ui.styles  import MAIN_CSS
from ui.sidebar import render_sidebar

# ── Page modules ──────────────────────────────────────────────────────────────
from page_modules.page_home      import render as render_home
from page_modules.page_profile   import render as render_profile
from page_modules.page_agents    import render as render_agents
from page_modules.page_resume    import render as render_resume
from page_modules.page_linkedin  import render as render_linkedin
from page_modules.page_skillgap  import render as render_skillgap
from page_modules.page_roadmap   import render as render_roadmap
from page_modules.page_chatbot   import render as render_chatbot
from page_modules.page_dashboard import render as render_dashboard
from page_modules.page_goals     import render as render_goals
from page_modules.page_about     import render as render_about


# ── Page Router ───────────────────────────────────────────────────────────────
PAGE_RENDERERS = {
    "home":      render_home,
    "profile":   render_profile,
    "agents":    render_agents,
    "resume":    render_resume,
    "linkedin":  render_linkedin,
    "skillgap":  render_skillgap,
    "roadmap":   render_roadmap,
    "chatbot":   render_chatbot,
    "dashboard": render_dashboard,
    "goals":     render_goals,
    "about":     render_about,
}


def main():
    # ── Inject custom CSS ──────────────────────────────────────────────────
    st.markdown(MAIN_CSS, unsafe_allow_html=True)

    # ── Initialise session state ───────────────────────────────────────────
    memory.init_session_state()

    # ── Render sidebar + get selected page ────────────────────────────────
    current_page = render_sidebar()

    # ── Render active page ────────────────────────────────────────────────
    renderer = PAGE_RENDERERS.get(current_page, render_home)
    renderer()


if __name__ == "__main__":
    main()
