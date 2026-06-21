# =============================================================================
# pages/page_chatbot.py  –  AI Chatbot with rich profile & analysis context
# =============================================================================

import streamlit as st
import utils.memory as memory
from ui.components import section_header, divider
from utils.llm_client import call_llm, is_ai_error
from utils.helpers import format_profile_for_prompt
from config.settings import CHATBOT_SYSTEM_PROMPT


def _build_prompt(user_message: str) -> str:
    """Build a context-rich prompt for the chatbot, including SWOT & Resume data."""
    profile      = memory.get_profile()
    profile_text = format_profile_for_prompt(profile) if profile else "No profile set yet."

    swot = memory.get_agent_output("profile_analyzer") or "SWOT analysis not run yet."
    resume_score = memory.get("resume_score", 0)
    skill_gap = memory.get("skill_gap_analysis") or "Skill gap analysis not run yet."

    context_additions = (
        f"\n\n--- ADDITIONAL CONTEXT ---"
        f"\nSWOT Analysis Results:\n{swot}"
        f"\nResume Score: {resume_score}/100"
        f"\nSkill Gap Assessment:\n{skill_gap}"
        f"\n--------------------------"
    )

    profile_enriched = profile_text + context_additions
    history_text     = memory.get_chat_context(max_messages=12)

    system = CHATBOT_SYSTEM_PROMPT.format(
        profile=profile_enriched,
        history=history_text or "No previous messages.",
    )
    return f"{system}\n\nStudent: {user_message}\nMentor AI:"


def render():
    st.markdown("""
    <div class="animate-in">
      <h2 style="margin-bottom:0.2rem; font-family:'Space Grotesk', sans-serif;">💬 Career Advisor Chatbot</h2>
      <p style="color:#64748B;margin-top:0;font-size:0.95rem;">
        Ask follow-up questions about your goals. The AI accesses your SWOT analysis and resume scores for contextual feedback.
      </p>
    </div>
    """, unsafe_allow_html=True)

    divider()

    profile    = memory.get_profile()
    career     = profile.get("career_goal", "my target career")
    branch     = profile.get("branch", "my field")
    suggestions = [
        f"What are the top skills I need for {career}?",
        f"How do I get my first internship in {branch}?",
        "Create a 30-day study plan for me.",
        "What certifications should I do first?",
        "How do I prepare for technical interviews?",
        "Review my career goal and suggest improvements.",
    ]

    section_header("Quick-start Inquiries", "💡")
    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(
                suggestion,
                key=f"suggestion_{i}",
                use_container_width=True,
            ):
                st.session_state["pending_message"] = suggestion

    divider()

    history = memory.get_chat_history()

    if not history:
        st.markdown("""
        <div style="text-align:center; padding:3rem 1rem; color:#94A3B8;" class="animate-in">
          <div style="font-size:3.5rem; margin-bottom:0.8rem;">🤖</div>
          <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.15rem; color:#64748B;">
            Interactive AI Career Mentor
          </div>
          <div style="font-size:0.88rem; margin-top:0.3rem;">
            Ask anything about salaries, skill gaps, or interview prep.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in history:
            role = msg["role"]
            with st.chat_message("user" if role == "user" else "assistant", avatar="👤" if role == "user" else "🕊️"):
                st.markdown(msg["content"])

    divider()

    pending = st.session_state.pop("pending_message", None)

    col_input, col_send = st.columns([5, 1])
    with col_input:
        user_input = st.text_input(
            "Message",
            value=pending or "",
            placeholder="Type a message or click one of the quick starter options above...",
            label_visibility="collapsed",
            key="chat_input_field",
        )
    with col_send:
        send_btn = st.button("Send 📨", type="primary", use_container_width=True, key="send_chat_btn")

    message_to_send = user_input.strip() if (send_btn and user_input.strip()) else None
    if pending and not send_btn:
        message_to_send = pending.strip()

    if message_to_send:
        prompt = _build_prompt(message_to_send)

        with st.spinner("🤖 Thinking..."):
            response = call_llm(prompt)

        memory.add_chat_message("user", message_to_send)
        memory.add_chat_message("assistant", response)

        if is_ai_error(response):
            st.error("The AI request failed. Check your Groq API key, or set LLM_GEMINI_FALLBACK=1 for Gemini fallback.")

        st.rerun()

    ctrl1, ctrl2, ctrl3 = st.columns(3)
    with ctrl1:
        if st.button("🗑️ Clear Chat History", use_container_width=True, key="clear_chat_page"):
            memory.clear_chat_history()
            st.rerun()
    with ctrl2:
        chat_text = "\n\n".join(
            [f"{'You' if m['role']=='user' else 'AI'}: {m['content']}" for m in history]
        )
        st.download_button(
            label="📥 Download Conversation",
            data=chat_text or "No chat history.",
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True,
            key="dl_chat",
        )
    with ctrl3:
        msg_count = len(history)
        st.markdown(
            f'<div style="text-align:center; font-size:0.85rem; color:#64748B; padding-top:0.6rem; font-weight:600;">'
            f'💬 {msg_count} messages in active context</div>',
            unsafe_allow_html=True,
        )
