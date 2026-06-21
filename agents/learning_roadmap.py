# =============================================================================
# agents/learning_roadmap.py  –  Agent 3: Learning Roadmap
# Generates a detailed 6-month month-by-month learning roadmap.
# =============================================================================

from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt
from config.settings import ROADMAP_PROMPT
import utils.memory as memory


def run_learning_roadmap(profile: dict, career: str = "") -> str:
    """
    Run the Learning Roadmap Agent.

    Args:
        profile: Student profile dictionary.
        career:  Target career string (optional; falls back to profile's career_goal).

    Returns:
        Markdown roadmap string.
    """
    if not profile:
        return "⚠️ No profile data found. Please complete your profile first."

    target_career = career or profile.get("career_goal", "Software Development")
    profile_text  = format_profile_for_prompt(profile)
    prompt        = ROADMAP_PROMPT.format(profile=profile_text, career=target_career)
    result        = call_llm(prompt)

    memory.save_agent_output("learning_roadmap", result)
    memory.set("roadmap_output", result)
    return result
