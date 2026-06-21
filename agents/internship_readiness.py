# =============================================================================
# agents/internship_readiness.py  –  Agent 5: Internship Readiness
# Evaluates how ready the student is for internships/jobs and what to fix.
# =============================================================================

from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt, extract_score_from_text
from config.settings import INTERNSHIP_READINESS_PROMPT
import utils.memory as memory


def run_internship_readiness(profile: dict) -> tuple[str, int]:
    """
    Run the Internship Readiness Agent.

    Args:
        profile: Student profile dictionary.

    Returns:
        Tuple of (markdown_result, readiness_score_int).
    """
    if not profile:
        return "⚠️ No profile data found. Please complete your profile first.", 0

    profile_text = format_profile_for_prompt(profile)
    prompt       = INTERNSHIP_READINESS_PROMPT.format(profile=profile_text)
    result       = call_llm(prompt)

    score = extract_score_from_text(result)
    memory.save_agent_output("internship_readiness", result)
    memory.set("internship_score", score)
    return result, score
