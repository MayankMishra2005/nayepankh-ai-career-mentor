# =============================================================================
# agents/career_mentor.py  –  Agent 2: Career Mentor
# Recommends career paths tailored to the student's profile.
# =============================================================================

from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt
from config.settings import CAREER_MENTOR_PROMPT
import utils.memory as memory


def run_career_mentor(profile: dict) -> str:
    """
    Run the Career Mentor Agent to suggest career paths.

    Args:
        profile: Student profile dictionary.

    Returns:
        Markdown string with career recommendations.
    """
    if not profile:
        return "⚠️ No profile data found. Please complete your profile first."

    profile_text = format_profile_for_prompt(profile)
    prompt = CAREER_MENTOR_PROMPT.format(profile=profile_text)
    result = call_llm(prompt)

    memory.save_agent_output("career_mentor", result)
    return result
