# =============================================================================
# ui/navigation.py
# Programmatic page navigation for the sidebar radio router.
# =============================================================================

import streamlit as st
from config.settings import PAGES


PAGE_KEY_TO_LABEL = {key: label for label, key in PAGES.items()}


def navigate_to(page_key: str) -> None:
    """Queue a page switch — applied in sidebar before the nav radio renders."""
    st.session_state["nav_page_override"] = page_key


def apply_nav_override() -> None:
    """Call from sidebar before st.radio so programmatic navigation works."""
    page_key = st.session_state.pop("nav_page_override", None)
    if not page_key:
        return
    label = PAGE_KEY_TO_LABEL.get(page_key)
    if label:
        st.session_state["nav_radio"] = label


def get_current_page_key() -> str:
    """Return the current page key from sidebar radio state."""
    label = st.session_state.get("nav_radio", list(PAGES.keys())[0])
    return PAGES.get(label, "home")
