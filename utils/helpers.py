# =============================================================================
# utils/helpers.py
# Miscellaneous helper functions for formatting, parsing, and display.
# =============================================================================

import re
import pandas as pd
from datetime import datetime


def format_profile_for_prompt(profile: dict) -> str:
    """Convert student profile dict to a readable string for AI prompts."""
    if not profile:
        return "No profile data available."
    lines = [
        f"Name: {profile.get('name', 'N/A')}",
        f"Degree: {profile.get('degree', 'N/A')}",
        f"Branch/Specialization: {profile.get('branch', 'N/A')}",
        f"Year of Study: {profile.get('year', 'N/A')}",
        f"Current Skills: {profile.get('skills', 'N/A')}",
        f"Interests: {profile.get('interests', 'N/A')}",
        f"Career Goal: {profile.get('career_goal', 'N/A')}",
        f"Preferred Industry: {profile.get('industry', 'N/A')}",
        f"Additional Info: {profile.get('additional_info', 'N/A')}",
    ]
    return "\n".join(lines)


def extract_score_from_text(text: str) -> int:
    """
    Extract a numeric score (e.g., '72/100' or 'Score: 72') from AI output text.
    Returns 0 if no score found.
    """
    patterns = [
        r'(\d{1,3})\s*/\s*100',
        r'Score[:\s]+(\d{1,3})',
        r'(\d{1,3})\s*out of\s*100',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            if 0 <= score <= 100:
                return score
    return 0


def parse_skills_list(skills_str: str) -> list[str]:
    """Parse a comma-separated or newline-separated skills string into a list."""
    if not skills_str:
        return []
    # Split by comma or newline, strip whitespace, filter empties
    parts = re.split(r'[,\n]', skills_str)
    return [p.strip() for p in parts if p.strip()]


def skills_to_tags_html(skills: list[str], color: str = "#1A56DB") -> str:
    """Convert a list of skills into HTML badge tags."""
    tags = []
    for skill in skills:
        tags.append(
            f'<span style="background:{color}15;color:{color};border:1px solid {color}40;'
            f'padding:3px 10px;border-radius:20px;font-size:0.82rem;'
            f'font-weight:600;margin:3px;display:inline-block;">{skill}</span>'
        )
    return " ".join(tags)


def score_to_color(score: int) -> str:
    """Return a color hex based on score value (0–100)."""
    if score >= 75:
        return "#059669"   # green
    elif score >= 50:
        return "#D97706"   # amber
    else:
        return "#DC2626"   # red


def score_to_emoji(score: int) -> str:
    """Return an emoji indicator for a score."""
    if score >= 80:
        return "🟢"
    elif score >= 55:
        return "🟡"
    else:
        return "🔴"


def score_to_label(score: int) -> str:
    """Return a text label for a score."""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 55:
        return "Average"
    elif score >= 35:
        return "Needs Work"
    else:
        return "Beginner"


def truncate_text(text: str, max_chars: int = 200) -> str:
    """Truncate text to max_chars and append ellipsis if needed."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + "…"


def get_greeting() -> str:
    """Return a time-appropriate greeting."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


def build_skills_dataframe(current_skills: list, missing_skills: list) -> pd.DataFrame:
    """Build a comparison DataFrame for skills visualization."""
    rows = []
    for skill in current_skills:
        rows.append({"Skill": skill, "Status": "✅ Have", "Priority": "Current"})
    for skill in missing_skills:
        rows.append({"Skill": skill, "Status": "❌ Missing", "Priority": "To Learn"})
    return pd.DataFrame(rows)


def sanitize_filename(name: str) -> str:
    """Make a string safe for use as a filename."""
    return re.sub(r'[^a-zA-Z0-9_\- ]', '', name).strip().replace(' ', '_')
