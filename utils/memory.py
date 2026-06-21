# =============================================================================
# utils/memory.py
# Session State memory manager for storing and retrieving student data.
# =============================================================================

import streamlit as st
from datetime import datetime

from utils.llm_client import is_ai_error


# ─── Default State Keys ───────────────────────────────────────────────────────
DEFAULTS = {
    "student_profile": {},
    "agent_outputs": {},
    "chat_history": [],
    "resume_analysis": None,
    "linkedin_analysis": None,
    "skill_gap_analysis": None,
    "roadmap_output": None,
    "resume_score": 0,
    "internship_score": 0,
    "linkedin_score": 0,
    "career_matches": [],
    "goals": [],
    "checklist": {},
    "current_page": "home",
    "onboarding_complete": False,
    "selected_career": "",
}


def init_session_state():
    """Initialize all session state keys with default values if not present."""
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def get(key: str, default=None):
    """Get a value from session state."""
    return st.session_state.get(key, default)


def set(key: str, value):
    """Set a value in session state."""
    st.session_state[key] = value
    
    # Sync shortcuts to agent outputs if applicable
    if key == "roadmap_output" and value:
        save_agent_output("learning_roadmap", value)
    elif key == "resume_analysis" and value:
        from utils.helpers import extract_score_from_text
        st.session_state["resume_score"] = extract_score_from_text(value)
    elif key == "linkedin_analysis" and value:
        from utils.helpers import extract_score_from_text
        st.session_state["linkedin_score"] = extract_score_from_text(value)


def update_profile(field: str, value):
    """Update a single field in the student profile dict."""
    if "student_profile" not in st.session_state:
        st.session_state["student_profile"] = {}
    st.session_state["student_profile"][field] = value


def get_profile() -> dict:
    """Return the full student profile dict."""
    return st.session_state.get("student_profile", {})


def profile_complete() -> bool:
    """Check if the minimum required profile fields are filled."""
    profile = get_profile()
    required = ["name", "degree", "branch", "year", "skills", "career_goal"]
    return all(profile.get(f) for f in required)


def save_agent_output(agent_name: str, output: str):
    """Save an agent's output with timestamp."""
    if "agent_outputs" not in st.session_state:
        st.session_state["agent_outputs"] = {}
    st.session_state["agent_outputs"][agent_name] = {
        "content": output,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    # Auto-synchronise with top-level shortcut keys
    if agent_name == "learning_roadmap":
        st.session_state["roadmap_output"] = output
    elif agent_name == "internship_readiness":
        from utils.helpers import extract_score_from_text
        score = extract_score_from_text(output)
        st.session_state["internship_score"] = score


def get_agent_output(agent_name: str) -> str | None:
    """Retrieve a successful agent output (excludes API error strings)."""
    outputs = st.session_state.get("agent_outputs", {})
    entry = outputs.get(agent_name)
    if not entry:
        return None
    content = entry.get("content")
    return content if is_valid_ai_output(content) else None


def get_agent_output_raw(agent_name: str) -> str | None:
    """Retrieve agent output including error strings (for display/debug)."""
    outputs = st.session_state.get("agent_outputs", {})
    entry = outputs.get(agent_name)
    return entry["content"] if entry else None


def is_valid_ai_output(text: str | None) -> bool:
    """True when text is a successful AI response (not an error string)."""
    if not text or not str(text).strip():
        return False
    return not is_ai_error(text)


def add_chat_message(role: str, content: str):
    """Append a message to the chat history."""
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    st.session_state["chat_history"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M"),
    })


def get_chat_history() -> list:
    """Return the full chat history list."""
    return st.session_state.get("chat_history", [])


def get_chat_context(max_messages: int = 10) -> str:
    """Return the last N chat messages as a formatted string for context injection."""
    history = get_chat_history()
    recent = history[-max_messages:] if len(history) > max_messages else history
    lines = []
    for msg in recent:
        role_label = "Student" if msg["role"] == "user" else "Mentor AI"
        lines.append(f"{role_label}: {msg['content']}")
    return "\n".join(lines)


def clear_chat_history():
    """Clear all chat messages."""
    st.session_state["chat_history"] = []


def clear_agent_outputs():
    """Clear all cached agent outputs and related derived state."""
    st.session_state["agent_outputs"] = {}
    st.session_state["roadmap_output"] = None
    st.session_state["resume_analysis"] = None
    st.session_state["linkedin_analysis"] = None
    st.session_state["skill_gap_analysis"] = None
    st.session_state["resume_score"] = 0
    st.session_state["internship_score"] = 0
    st.session_state["linkedin_score"] = 0


def clear_all_memory():
    """Full reset — clears all session state."""
    for key, default in DEFAULTS.items():
        if isinstance(default, dict):
            st.session_state[key] = {}
        elif isinstance(default, list):
            st.session_state[key] = []
        else:
            st.session_state[key] = default


def add_goal(goal_text: str):
    """Add a new goal to the goals list."""
    if "goals" not in st.session_state:
        st.session_state["goals"] = []
    st.session_state["goals"].append({
        "text": goal_text,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d"),
    })


def toggle_goal(index: int):
    """Toggle completion status of a goal."""
    goals = st.session_state.get("goals", [])
    if 0 <= index < len(goals):
        goals[index]["done"] = not goals[index]["done"]
        st.session_state["goals"] = goals


def remove_goal(index: int):
    """Remove a goal by index."""
    goals = st.session_state.get("goals", [])
    if 0 <= index < len(goals):
        goals.pop(index)
        st.session_state["goals"] = goals
