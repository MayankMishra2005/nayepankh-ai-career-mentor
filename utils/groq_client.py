# =============================================================================
# utils/groq_client.py
# Primary LLM provider — Groq API wrapper (shared by all agents).
# =============================================================================

import os
import time
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from groq import Groq
from config.settings import (
    GROQ_MODEL,
    GROQ_FALLBACK_MODELS,
    GROQ_MAX_TOKENS,
    GROQ_TEMPERATURE,
)


def get_api_key() -> str | None:
    """Retrieve Groq API key from Streamlit secrets or environment variable."""
    try:
        key = st.secrets["GROQ_API_KEY"]
        if key and str(key).strip():
            return str(key).strip()
    except (KeyError, FileNotFoundError, AttributeError, TypeError):
        pass

    key = os.getenv("GROQ_API_KEY", "").strip()
    return key or None


def get_client() -> Groq | None:
    """Create a Groq client. Returns None if no API key is configured."""
    key = get_api_key()
    if not key:
        return None
    return Groq(api_key=key)


def is_ai_error(text: str | None) -> bool:
    """Return True if text looks like an API/configuration error, not AI content."""
    if not text or not str(text).strip():
        return True
    markers = (
        "🔑 **Groq API key",
        "🔑 **Gemini API key",
        "🔑 **Invalid API key",
        "⏳ **API quota exceeded",
        "⚠️ **Model not available",
        "❌ **API Error",
        "❌ **Groq API Error",
        "API key not configured",
        "GROQ_API_KEY",
        "Traceback (most recent call last)",
    )
    sample = str(text)[:400]
    return any(m in sample for m in markers)


def _models_to_try() -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for name in [GROQ_MODEL, *GROQ_FALLBACK_MODELS]:
        if name and name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def _format_api_error(error: Exception) -> str:
    msg = str(error)
    if "401" in msg or "403" in msg or "invalid_api_key" in msg.lower():
        return (
            "🔑 **Groq API key invalid.** Check `GROQ_API_KEY` in your `.env` file.\n\n"
            "Get a key at [Groq Console](https://console.groq.com/keys)."
        )
    if "429" in msg or "rate_limit" in msg.lower():
        return (
            "⏳ **Groq rate limit reached.** Wait a moment and try again.\n\n"
            f"Details: {msg}"
        )
    if "404" in msg or "model" in msg.lower() and "not found" in msg.lower():
        return (
            f"⚠️ **Groq model not available.** {msg}\n\n"
            "Update `GROQ_MODEL` in `config/settings.py`."
        )
    return f"❌ **Groq API Error:** {msg}"


def call_groq(prompt: str, retries: int = 3, delay: float = 1.5) -> str:
    """
    Call the Groq chat completions API with a given prompt.

    Tries primary model then fallbacks. Returns AI text or an error string.
    """
    if not prompt or not prompt.strip():
        return "⚠️ Empty prompt provided. Please fill in your profile details first."

    client = get_client()
    if not client:
        return (
            "🔑 **Groq API key not configured.**\n\n"
            "Add your key to the `.env` file:\n"
            "`GROQ_API_KEY=your_key_here`\n\n"
            "Get a free key at [Groq Console](https://console.groq.com/keys)."
        )

    last_error: Exception | None = None
    for model in _models_to_try():
        for attempt in range(retries):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=GROQ_MAX_TOKENS,
                    temperature=GROQ_TEMPERATURE,
                )
                text = response.choices[0].message.content
                if text and text.strip():
                    return text.strip()
                return "⚠️ The AI was unable to generate a response for this input."
            except Exception as e:
                last_error = e
                err_text = str(e)
                if "404" in err_text or ("model" in err_text.lower() and "not found" in err_text.lower()):
                    break
                if any(token in err_text for token in ("401", "403", "invalid_api_key")):
                    return _format_api_error(e)
                if attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))

    return _format_api_error(last_error or RuntimeError("Unknown Groq API error"))


def call_groq_streaming(prompt: str):
    """Generator that yields streamed Groq response chunks."""
    if not prompt or not prompt.strip():
        yield "⚠️ Empty prompt provided."
        return

    client = get_client()
    if not client:
        yield "🔑 **Groq API key not configured.** Add `GROQ_API_KEY` to your `.env` file."
        return

    for model in _models_to_try():
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=GROQ_MAX_TOKENS,
                temperature=GROQ_TEMPERATURE,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
            return
        except Exception as e:
            err_text = str(e)
            if "404" in err_text or ("model" in err_text.lower() and "not found" in err_text.lower()):
                continue
            yield _format_api_error(e)
            return

    yield _format_api_error(RuntimeError("All configured Groq models failed."))


def verify_api_connection() -> tuple[bool, str]:
    """Lightweight Groq health check. Returns (success, message)."""
    if not get_api_key():
        return False, "Groq API key missing — add GROQ_API_KEY to .env"

    client = get_client()
    if not client:
        return False, "Could not initialize Groq client"

    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": "Reply with exactly: OK"}],
            max_tokens=16,
            temperature=0,
        )
        text = response.choices[0].message.content
        if text:
            return True, f"Groq connected ({GROQ_MODEL})"
        return False, "Groq returned empty response"
    except Exception as e:
        return False, f"Groq error: {e}"
