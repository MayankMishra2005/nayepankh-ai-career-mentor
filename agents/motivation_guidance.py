# =============================================================================
# agents/motivation_guidance.py  –  Agent 6: Motivation & Guidance
# Provides personalised encouragement and next-step advice.
# =============================================================================

from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt
from config.settings import MOTIVATION_PROMPT
import utils.memory as memory


def run_motivation_guidance(profile: dict) -> str:
    """
    Run the Motivation & Guidance Agent.

    Args:
        profile: Student profile dictionary.

    Returns:
        Markdown motivational guidance string.
    """
    if not profile:
        return "⚠️ No profile data found. Please complete your profile first."

    profile_text = format_profile_for_prompt(profile)
    context      = memory.get_chat_context(max_messages=6)
    name         = profile.get("name", "Student")

    prompt = MOTIVATION_PROMPT.format(
        profile=profile_text,
        context=context or "No previous conversation.",
        name=name,
    )
    result = call_llm(prompt)

    memory.save_agent_output("motivation_guidance", result)
    return result
