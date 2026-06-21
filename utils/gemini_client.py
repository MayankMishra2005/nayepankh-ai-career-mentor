# =============================================================================
# utils/gemini_client.py
# Unified Gemini API wrapper using the google-genai SDK.
# =============================================================================

import os
import time
import traceback
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from google import genai
from google.genai import types
from config.settings import (
    GEMINI_MODEL,
    GEMINI_FALLBACK_MODELS,
    GEMINI_MAX_TOKENS,
    GEMINI_TEMPERATURE,
)

# Set GEMINI_DEBUG=1 in .env to surface raw exceptions (no friendly masking)
_DEBUG = os.getenv("GEMINI_DEBUG", "").strip().lower() in ("1", "true", "yes")


def _dump_raw_api_error(error: Exception) -> str:
    """Print and return the exact SDK exception — no friendly masking."""
    import json

    parts: list[str] = []
    parts.append("=== GEMINI RAW API ERROR (GEMINI_DEBUG=1) ===")
    parts.append("")
    parts.append("=== EXCEPTION TYPE ===")
    parts.append(repr(type(error)))
    parts.append("")
    parts.append("=== EXCEPTION STR (exact SDK) ===")
    parts.append(str(error))
    parts.append("")
    parts.append("=== EXCEPTION REPR (exact SDK) ===")
    parts.append(repr(error))
    parts.append("")
    parts.append("=== TRACEBACK ===")
    parts.append(traceback.format_exc())

    if hasattr(error, "code"):
        parts.append("")
        parts.append("=== HTTP STATUS CODE ===")
        parts.append(str(getattr(error, "code")))

    if hasattr(error, "status") and getattr(error, "status", None) is not None:
        parts.append("")
        parts.append("=== STATUS ===")
        parts.append(str(getattr(error, "status")))

    if hasattr(error, "message") and getattr(error, "message", None) is not None:
        parts.append("")
        parts.append("=== MESSAGE ===")
        parts.append(str(getattr(error, "message")))

    if hasattr(error, "details"):
        parts.append("")
        parts.append("=== RESPONSE BODY (error.details) ===")
        try:
            parts.append(json.dumps(getattr(error, "details"), indent=2, default=str))
        except TypeError:
            parts.append(repr(getattr(error, "details")))

    response = getattr(error, "response", None)
    if response is not None:
        parts.append("")
        parts.append("=== RAW HTTP RESPONSE OBJECT ===")
        parts.append(repr(response))
        if hasattr(response, "text"):
            parts.append("")
            parts.append("=== RAW HTTP RESPONSE TEXT ===")
            parts.append(response.text)
        if hasattr(response, "status_code"):
            parts.append("")
            parts.append("=== RAW HTTP response.status_code ===")
            parts.append(str(response.status_code))

    dump = "\n".join(parts)
    print(dump, flush=True)
    return dump


def get_api_key() -> str | None:
    """Retrieve Gemini API key from Streamlit secrets or environment variable."""
    try:
        key = st.secrets["GEMINI_API_KEY"]
        if key and str(key).strip():
            return str(key).strip()
    except (KeyError, FileNotFoundError, AttributeError, TypeError):
        pass

    key = os.getenv("GEMINI_API_KEY", "").strip()
    return key or None


def get_client() -> genai.Client | None:
    """Create a Gemini client. Returns None if no API key is configured."""
    key = get_api_key()
    if not key:
        return None
    try:
        return genai.Client(api_key=key)
    except Exception:
        if _DEBUG:
            raise
        return None


def is_ai_error(text: str | None) -> bool:
    """Return True if text looks like an API/configuration error, not AI content."""
    if not text or not str(text).strip():
        return True
    markers = (
        "🔑 **Gemini API key",
        "🔑 **Invalid API key",
        "⏳ **API quota exceeded",
        "⚠️ **Model not available",
        "❌ **API Error",
        "API key not configured",
        "Traceback (most recent call last)",
    )
    sample = str(text)[:400]
    return any(m in sample for m in markers)


def _generation_config() -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        max_output_tokens=GEMINI_MAX_TOKENS,
        temperature=GEMINI_TEMPERATURE,
    )


def _format_api_error(error: Exception) -> str:
    """Turn raw API exceptions into user-friendly messages (production mode)."""
    if _DEBUG:
        return _dump_raw_api_error(error)

    msg = str(error)

    if "404" in msg or "NOT_FOUND" in msg or "not found" in msg.lower():
        return (
            "⚠️ **Model not available.** The configured Gemini model could not be found.\n\n"
            "Update `GEMINI_MODEL` in `config/settings.py` to a current model "
            "(e.g. `gemini-2.0-flash`)."
        )

    if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower():
        return (
            "⏳ **API quota exceeded.** Your Gemini API key has hit its usage limit.\n\n"
            "Wait a few minutes and try again, or check your quota at "
            "[Google AI Studio](https://aistudio.google.com/apikey)."
        )

    if "401" in msg or "403" in msg or "API_KEY" in msg or "permission" in msg.lower():
        return (
            "🔑 **Invalid API key.** Gemini rejected the configured API key.\n\n"
            "Get a valid key from [Google AI Studio](https://aistudio.google.com/apikey) "
            "and set it as `GEMINI_API_KEY` in your `.env` file."
        )

    return (
        f"❌ **API Error:** {msg}\n\n"
        "Set `GEMINI_DEBUG=1` in `.env` for full traceback details."
    )


def _models_to_try() -> list[str]:
    """Primary model first, then fallbacks (deduplicated)."""
    seen: set[str] = set()
    ordered: list[str] = []
    for name in [GEMINI_MODEL, *GEMINI_FALLBACK_MODELS]:
        if name and name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def _generate_once(client: genai.Client, prompt: str, model: str) -> str:
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=_generation_config(),
    )
    text = getattr(response, "text", None)
    if text:
        return text
    return "⚠️ The AI was unable to generate a response for this input."


def call_gemini(prompt: str, retries: int = 3, delay: float = 2.0) -> str:
    """
    Call the Gemini API with a given prompt.

    Tries the primary model, then fallbacks. Retries on transient errors.
    """
    if not prompt or not prompt.strip():
        return "⚠️ Empty prompt provided. Please fill in your profile details first."

    client = get_client()
    if not client:
        return (
            "🔑 **Gemini API key not configured.**\n\n"
            "Add your key to the `.env` file:\n"
            "`GEMINI_API_KEY=your_key_here`\n\n"
            "Get a free key at [Google AI Studio](https://aistudio.google.com/apikey)."
        )

    if _DEBUG:
        api_key = get_api_key()
        if api_key:
            print("API KEY PREFIX:", api_key[:10], flush=True)

    models = _models_to_try()
    last_error: Exception | None = None

    for model in models:
        for attempt in range(retries):
            try:
                return _generate_once(client, prompt, model)
            except Exception as e:
                last_error = e
                if _DEBUG:
                    _dump_raw_api_error(e)
                    raise
                err_text = str(e)
                # Don't retry on auth / quota; try next model on 404 only
                if any(
                    token in err_text
                    for token in ("401", "403", "429", "RESOURCE_EXHAUSTED", "API_KEY")
                ):
                    return _format_api_error(e)
                if "404" in err_text or "NOT_FOUND" in err_text:
                    break  # try next fallback model
                if attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))

    return _format_api_error(last_error or RuntimeError("Unknown API error"))


def call_gemini_streaming(prompt: str):
    """Generator that yields streamed Gemini response chunks."""
    if not prompt or not prompt.strip():
        yield "⚠️ Empty prompt provided."
        return

    client = get_client()
    if not client:
        yield (
            "🔑 **Gemini API key not configured.**\n\n"
            "Add `GEMINI_API_KEY=your_key_here` to your `.env` file."
        )
        return

    for model in _models_to_try():
        try:
            stream = client.models.generate_content_stream(
                model=model,
                contents=prompt,
                config=_generation_config(),
            )
            for chunk in stream:
                text = getattr(chunk, "text", None)
                if text:
                    yield text
            return
        except Exception as e:
            if _DEBUG:
                _dump_raw_api_error(e)
                raise
            err_text = str(e)
            if "404" in err_text or "NOT_FOUND" in err_text:
                continue
            yield _format_api_error(e)
            return

    yield _format_api_error(RuntimeError("All configured models failed."))


def verify_api_connection() -> tuple[bool, str]:
    """
    Lightweight API health check. Returns (success, message).
    Used by sidebar status indicator.
    """
    if not get_api_key():
        return False, "API key missing — add GEMINI_API_KEY to .env"

    client = get_client()
    if not client:
        return False, "Could not initialize Gemini client"

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents="Reply with exactly: OK",
            config=types.GenerateContentConfig(max_output_tokens=16, temperature=0),
        )
        if getattr(response, "text", None):
            return True, f"Connected ({GEMINI_MODEL})"
        return False, "API returned empty response"
    except Exception as e:
        if _DEBUG:
            _dump_raw_api_error(e)
            return False, str(e)
        err = str(e)
        if "429" in err or "quota" in err.lower():
            return True, "Key valid (quota limit — wait and retry)"
        if "404" in err or "NOT_FOUND" in err:
            return False, f"Model '{GEMINI_MODEL}' not found"
        if "401" in err or "403" in err or "API_KEY" in err:
            return False, "Invalid API key"
        return False, "Connection failed — check network and key"
