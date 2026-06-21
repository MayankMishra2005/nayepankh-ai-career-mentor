# =============================================================================
# modules/linkedin_reviewer.py
# LinkedIn profile text analysis using Gemini AI.
# =============================================================================

from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt, extract_score_from_text
from config.settings import LINKEDIN_REVIEWER_PROMPT
import utils.memory as memory


def analyze_linkedin(linkedin_text: str, profile: dict) -> tuple[str, int]:
    """
    Analyze pasted LinkedIn profile information.

    Args:
        linkedin_text: Raw text the student pasted from their LinkedIn profile.
        profile:       Student profile dict for context.

    Returns:
        Tuple of (analysis_markdown, profile_strength_score).
    """
    if not linkedin_text or not linkedin_text.strip():
        return "⚠️ No LinkedIn content provided. Please paste your profile information.", 0

    profile_text = format_profile_for_prompt(profile)
    prompt = LINKEDIN_REVIEWER_PROMPT.format(
        linkedin_text=linkedin_text[:5000],
        profile=profile_text,
    )
    result = call_llm(prompt)
    score  = extract_score_from_text(result)

    memory.set("linkedin_analysis", result)
    return result, score


def get_linkedin_paste_instructions() -> str:
    """Return markdown instructions for how to copy LinkedIn profile info."""
    return """
**How to copy your LinkedIn profile info:**
1. Open your LinkedIn profile in a browser
2. Copy your **Headline**, **About section**, **Experience**, **Skills**, and **Education**
3. Paste everything into the text box below
4. The AI will analyze and suggest improvements

> 💡 **Tip:** Include as much detail as possible for a more accurate review.
"""
