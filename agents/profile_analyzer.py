# =============================================================================
# agents/profile_analyzer.py  –  Agent 1: Profile Analyzer
# Analyzes student profile and generates a SWOT-style summary.
# =============================================================================

from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt
from config.settings import PROFILE_ANALYZER_PROMPT
import utils.memory as memory


def run_profile_analyzer(profile: dict) -> str:
    """
    Run the Profile Analyzer Agent on the given student profile.

    Args:
        profile: Student profile dictionary.

    Returns:
        Markdown string with profile analysis.
    """
    if not profile:
        return "⚠️ No profile data found. Please complete your profile first."

    profile_text = format_profile_for_prompt(profile)
    prompt = PROFILE_ANALYZER_PROMPT.format(profile=profile_text)
    result = call_llm(prompt)

    # Cache the result in session memory
    memory.save_agent_output("profile_analyzer", result)
    return result
