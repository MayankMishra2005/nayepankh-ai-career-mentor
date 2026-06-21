# =============================================================================
# modules/skill_gap.py
# Skill gap analysis: compares current skills vs. target career requirements.
# =============================================================================

from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt
from config.settings import SKILL_GAP_PROMPT
import utils.memory as memory


def run_skill_gap_analysis(
    profile: dict,
    target_career: str = "",
    target_industry: str = "",
) -> str:
    """
    Perform a skill gap analysis between current skills and target career.

    Args:
        profile:         Student profile dictionary.
        target_career:   Target career title (defaults to profile's career_goal).
        target_industry: Target industry (defaults to profile's industry).

    Returns:
        Markdown analysis string.
    """
    if not profile:
        return "⚠️ No profile data found. Please complete your profile first."

    current_skills = profile.get("skills", "Not specified")
    career         = target_career or profile.get("career_goal", "Software Engineering")
    industry       = target_industry or profile.get("industry", "Technology / Software")
    profile_text   = format_profile_for_prompt(profile)

    prompt = SKILL_GAP_PROMPT.format(
        current_skills=current_skills,
        target_career=career,
        target_industry=industry,
        profile=profile_text,
    )
    result = call_llm(prompt)
    memory.set("skill_gap_analysis", result)
    return result
