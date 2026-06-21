# =============================================================================
# modules/resume_analyzer.py
# PDF text extraction + Gemini-powered resume analysis + scoring.
# =============================================================================

import io
import streamlit as st
from utils.llm_client import call_llm
from utils.helpers import format_profile_for_prompt, extract_score_from_text
from config.settings import RESUME_ANALYZER_PROMPT
import utils.memory as memory


# ─── PDF Text Extraction ──────────────────────────────────────────────────────

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract raw text from an uploaded PDF file.
    Tries pdfplumber first, falls back to PyPDF2.

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        Extracted text string.
    """
    text = ""

    # Try pdfplumber (better formatting)
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text.strip()
    except Exception:
        pass

    # Reset file pointer and try PyPDF2
    try:
        uploaded_file.seek(0)
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        return f"❌ Could not read PDF: {str(e)}"

    return text.strip() if text.strip() else "❌ No readable text found in the PDF."


# ─── Resume Analysis ──────────────────────────────────────────────────────────

def analyze_resume(resume_text: str, profile: dict) -> tuple[str, int]:
    """
    Analyze resume text with Gemini and extract a score.

    Args:
        resume_text: Raw text extracted from the PDF.
        profile:     Student profile dictionary for context.

    Returns:
        Tuple of (analysis_markdown, score_int).
    """
    if not resume_text or resume_text.startswith("❌"):
        return "⚠️ Could not extract text from the resume. Please try a different PDF.", 0

    profile_text = format_profile_for_prompt(profile)
    prompt = RESUME_ANALYZER_PROMPT.format(
        resume_text=resume_text[:6000],   # Truncate to avoid token limits
        profile=profile_text,
    )
    result = call_llm(prompt)
    score  = extract_score_from_text(result)

    # Cache results
    memory.set("resume_analysis", result)
    memory.set("resume_score", score)
    return result, score


# ─── Streamlit Upload Widget ──────────────────────────────────────────────────

def render_resume_upload() -> tuple[str | None, object | None]:
    """
    Render the resume upload widget.

    Returns:
        Tuple of (extracted_text or None, uploaded_file or None).
    """
    st.markdown("""
    <div style="background:#F0F9FF;border:2px dashed #93C5FD;border-radius:12px;
                padding:1.5rem;text-align:center;margin-bottom:1rem;">
      <div style="font-size:2rem;margin-bottom:0.4rem;">📄</div>
      <div style="font-weight:600;color:#1E40AF;margin-bottom:0.3rem;">Upload Your Resume</div>
      <div style="font-size:0.83rem;color:#64748B;">PDF format • Max 10 MB</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        label="Choose PDF file",
        type=["pdf"],
        label_visibility="collapsed",
        key="resume_uploader",
    )

    if uploaded:
        with st.spinner("📖 Reading your resume..."):
            text = extract_text_from_pdf(uploaded)
        if text.startswith("❌"):
            st.error(text)
            return None, None
        st.success(f"✅ Resume loaded — {len(text.split())} words extracted")
        with st.expander("👁️ Preview extracted text"):
            st.text(text[:2000] + ("…" if len(text) > 2000 else ""))
        return text, uploaded

    return None, None
