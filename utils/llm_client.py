# =============================================================================
# utils/llm_client.py
# Unified LLM entry point: Groq (primary) → Gemini (optional fallback).
# All agents and modules should import from here.
# =============================================================================

import os

from utils.groq_client import (
    call_groq,
    call_groq_streaming,
    get_api_key as get_groq_api_key,
    is_ai_error,
    verify_api_connection as verify_groq_connection,
)


def _gemini_fallback_enabled() -> bool:
    flag = os.getenv("LLM_GEMINI_FALLBACK", "0").strip().lower()
    if flag not in ("1", "true", "yes"):
        return False
    try:
        from utils.gemini_client import get_api_key as get_gemini_api_key
        return bool(get_gemini_api_key())
    except Exception:
        return False


def get_api_key() -> str | None:
    """Return the active primary (Groq) API key."""
    return get_groq_api_key()


def call_llm(prompt: str, retries: int = 3, delay: float = 1.5) -> str:
    """
    Generate text using Groq. Optionally falls back to Gemini when
    LLM_GEMINI_FALLBACK=1 and GROQ returns an error.
    """
    result = call_groq(prompt, retries=retries, delay=delay)
    if not is_ai_error(result):
        return result

    if _gemini_fallback_enabled():
        from utils.gemini_client import call_gemini
        fallback = call_gemini(prompt, retries=retries, delay=delay)
        if not is_ai_error(fallback):
            return fallback

    return result


def call_llm_streaming(prompt: str):
    """Stream text from Groq (no Gemini streaming fallback)."""
    yield from call_groq_streaming(prompt)


def verify_api_connection() -> tuple[bool, str]:
    """Verify Groq connectivity; optionally report Gemini fallback availability."""
    ok, msg = verify_groq_connection()
    if ok:
        return ok, msg
    if _gemini_fallback_enabled():
        from utils.gemini_client import verify_api_connection as verify_gemini
        g_ok, g_msg = verify_gemini()
        if g_ok:
            return True, f"Groq unavailable; Gemini fallback active ({g_msg})"
    return ok, msg


# Backward-compatible alias used during migration
call_gemini = call_llm
