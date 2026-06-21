# =============================================================================
# ui/components.py
# Reusable UI building blocks: cards, metrics, badges, progress bars, etc.
# Upgraded for visual excellence and interactive dashboard aesthetics.
# =============================================================================

import streamlit as st
import math
import time
from utils.helpers import score_to_color, score_to_emoji, score_to_label


# ─── Premium Metric Card ─────────────────────────────────────────────────────

def premium_metric_card(label: str, value: str, sub: str = "", icon: str = "📈", color: str = "#3B82F6"):
    """Render a premium styled metric card with glow hover effect."""
    st.markdown(f"""
    <div class="np-metric animate-in">
      <div class="metric-icon-wrap" style="background:{color}0D; border-color:{color}2A; color:{color};">
        {icon}
      </div>
      <div class="metric-value">{value}</div>
      <div class="metric-label">{label}</div>
      {"<div class='metric-sub'>" + sub + "</div>" if sub else ""}
    </div>
    """, unsafe_allow_html=True)


# ─── SVG Radial / Ring Score Bar ──────────────────────────────────────────────

def radial_score_bar(label: str, score: int, icon: str = "📊"):
    """Render a beautiful circular score bar using inline SVG."""
    color = score_to_color(score)
    emoji = score_to_emoji(score)
    rating = score_to_label(score)
    
    # SVG parameters: Radius = 38, Circumference = 2 * pi * 38 ≈ 238.76
    circ = 238.76
    offset = circ * (1 - min(max(score, 0), 100) / 100)
    
    st.markdown(f"""
    <div class="np-card np-card-glow-blue animate-in" style="padding: 1.25rem 1.5rem;">
      <div class="ring-container">
        <div class="ring-svg-wrap">
          <svg width="90" height="90">
            <circle class="ring-bg" cx="45" cy="45" r="38"></circle>
            <circle class="ring-fill" cx="45" cy="45" r="38" 
                    style="stroke:{color}; stroke-dasharray:{circ}; stroke-dashoffset:{offset};">
            </circle>
          </svg>
          <div class="ring-text" style="color:{color};">{score}</div>
        </div>
        <div>
          <div style="font-weight:700; font-size:1rem; color:#0F172A; display:flex; align-items:center; gap:0.4rem;">
            <span style="font-size:1.2rem;">{icon}</span> {label}
          </div>
          <div style="font-size:0.8rem; color:{color}; font-weight:700; margin-top:4px; display:flex; align-items:center; gap:0.25rem;">
            <span>{emoji}</span> <span>{rating}</span>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Interactive Workflow Pipeline Visualizer ────────────────────────────────

def workflow_visualization(active_key: str, completed_keys: list[str]):
    """
    Renders an interactive, step-by-step visual pipeline of the 6 agents.
    
    Args:
        active_key: The key of the agent currently running or selected.
        completed_keys: List of keys of agents that have already completed execution.
    """
    agents = [
        {"key": "profile_analyzer",    "icon": "🧠", "short": "SWOT"},
        {"key": "career_mentor",       "icon": "🎯", "short": "Mentor"},
        {"key": "learning_roadmap",    "icon": "🗺️", "short": "Roadmap"},
        {"key": "project_recommender", "icon": "🏗️", "short": "Projects"},
        {"key": "internship_readiness","icon": "💼", "short": "Ready"},
        {"key": "motivation_guidance", "icon": "🌟", "short": "Growth"},
    ]
    
    html = '<div class="flow-container animate-in">'
    
    for i, agent in enumerate(agents):
        key = agent["key"]
        icon = agent["icon"]
        lbl = agent["short"]
        
        # Determine step state class
        is_completed = key in completed_keys
        is_active = key == active_key
        
        step_class = ""
        if is_completed:
            step_class = "completed"
        elif is_active:
            step_class = "active"
            
        html += f"""
        <div class="flow-step {step_class}">
          <div class="flow-icon-wrap">{icon}</div>
          <div class="flow-label">{lbl}</div>
        </div>
        """
        
        # Draw connection line if not the last step
        if i < len(agents) - 1:
            conn_class = ""
            if is_completed:
                conn_class = "completed"
            elif is_active:
                conn_class = "active"
            html += f'<div class="flow-connector {conn_class}"></div>'
            
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


# ─── Simulated Developer Terminal Console ────────────────────────────────────

def terminal_console(logs: list):
    """
    Renders a scrolling monospace developer console.
    
    Args:
        logs: A list of dicts/tuples or strings: e.g. [{"time": "12:00", "type": "info", "msg": "text"}]
    """
    lines_html = ""
    for log in logs:
        if isinstance(log, dict):
            timestamp = log.get("time", "")
            log_type = log.get("type", "info")
            msg = log.get("msg", "")
        elif isinstance(log, tuple) and len(log) == 3:
            timestamp, log_type, msg = log
        else:
            timestamp = ""
            log_type = "info"
            msg = str(log)
            
        type_class = f"terminal-{log_type}"
        ts_html = f'<span class="terminal-timestamp">[{timestamp}]</span>' if timestamp else ""
        lines_html += f"""
        <div class="terminal-line">
          {ts_html}
          <span class="{type_class}">&gt; {msg}</span>
        </div>
        """
        
    st.markdown(f"""
    <div class="terminal-console animate-in">
      <div class="terminal-header">
        <div class="terminal-dot terminal-red"></div>
        <div class="terminal-dot terminal-yellow"></div>
        <div class="terminal-dot terminal-green"></div>
        <span style="color:#64748B; font-size:0.75rem; margin-left:0.6rem; font-weight:700;">AI Pipeline System Log</span>
      </div>
      {lines_html}
      <div class="terminal-line"><span class="terminal-blink"></span></div>
    </div>
    """, unsafe_allow_html=True)


# ─── Legacy/Updated Components for compatibility ────────────────────────────

def metric_card(label: str, value: str, sub: str = "", color: str = "#3B82F6", icon: str = ""):
    """Render a styled metric card using the upgraded design system."""
    premium_metric_card(label, value, sub, icon or "📈", color)


def score_card(label: str, score: int, icon: str = "📊"):
    """Render a score card with upgraded styling and visual progress line."""
    color  = score_to_color(score)
    emoji  = score_to_emoji(score)
    lbl    = score_to_label(score)
    pct    = max(0, min(score, 100))
    st.markdown(f"""
    <div class="np-card animate-in" style="border-left: 4px solid {color}; padding: 1.25rem 1.5rem;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:0.78rem; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:0.05em;">{label}</div>
          <div style="font-family:'Space Grotesk', sans-serif; font-size:1.8rem; font-weight:700; color:#0F172A; margin-top:0.25rem;">
            {score}<span style="font-size:0.9rem; color:#94A3B8; font-weight:500;">/100</span>
          </div>
        </div>
        <div style="font-size:2.2rem; filter:drop-shadow(0 2px 6px rgba(0,0,0,0.05));">{icon}</div>
      </div>
      <div style="margin-top:0.75rem;">
        <div class="np-progress-wrap" style="height: 6px;">
          <div class="np-progress-fill" style="width:{pct}%; background:{color};"></div>
        </div>
        <div style="font-size:0.78rem; color:{color}; font-weight:700; margin-top:4px; display:flex; align-items:center; gap:0.25rem;">
          <span>{emoji}</span> <span>{lbl}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, icon: str = ""):
    """Render a styled section header with upgraded typography."""
    st.markdown(f"""
    <div class="np-section-header animate-in">
      <span class="section-icon">{icon}</span>
      <span class="section-title">{title}</span>
    </div>
    """, unsafe_allow_html=True)


def agent_card(agent_name: str, agent_icon: str, content: str, color: str = "#3B82F6"):
    """Render an agent result card with premium design."""
    st.markdown(f"""
    <div class="np-card animate-in" style="border-left:4px solid {color};">
      <div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1rem;">
        <span style="font-size:1.4rem; padding:0.4rem; background:{color}0F; border-radius:8px;">{agent_icon}</span>
        <strong style="font-family:'Space Grotesk', sans-serif; font-size:1.1rem; color:{color};">{agent_name}</strong>
      </div>
      <div class="agent-card-content" style="font-size:0.92rem; line-height:1.6; color:#334155;">
    """, unsafe_allow_html=True)
    st.markdown(content)
    st.markdown("</div></div>", unsafe_allow_html=True)


def info_box(message: str, icon: str = "ℹ️"):
    st.markdown(f'<div class="np-info-box animate-in"><span>{icon}</span><span>{message}</span></div>', unsafe_allow_html=True)


def warning_box(message: str, icon: str = "⚠️"):
    st.markdown(f'<div class="np-warning-box animate-in"><span>{icon}</span><span>{message}</span></div>', unsafe_allow_html=True)


def success_box(message: str, icon: str = "✅"):
    st.markdown(f'<div class="np-success-box animate-in"><span>{icon}</span><span>{message}</span></div>', unsafe_allow_html=True)


def skill_tags(skills: list[str], color: str = "#3B82F6"):
    """Render a list of skills as colorful inline tags with custom borders."""
    if not skills:
        st.markdown('<span style="color:#94A3B8; font-size:0.85rem; font-style:italic;">No items listed yet.</span>', unsafe_allow_html=True)
        return
    tags_html = ""
    for skill in skills:
        tags_html += (
            f'<span style="background:{color}0D; color:{color}; border:1px solid {color}2A;'
            f'padding:5px 14px; border-radius:20px; font-size:0.8rem; font-weight:600;'
            f'margin:4px; display:inline-block; box-shadow:0 1px 3px rgba(0,0,0,0.01);">#{skill}</span>'
        )
    st.markdown(f'<div style="line-height:2.4;">{tags_html}</div>', unsafe_allow_html=True)


def progress_bar(label: str, value: int, max_val: int = 100, color: str = "#3B82F6"):
    """Render a labeled progress bar with details."""
    pct = int((value / max_val) * 100) if max_val > 0 else 0
    st.markdown(f"""
    <div style="margin-bottom:1rem;" class="animate-in">
      <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
        <span style="font-size:0.85rem; font-weight:600; color:#334155;">{label}</span>
        <span style="font-size:0.85rem; font-weight:700; color:{color};">{value}/{max_val}</span>
      </div>
      <div class="np-progress-wrap" style="height: 8px;">
        <div class="np-progress-fill" style="width:{pct}%; background:linear-gradient(90deg, {color}, {color}BB);"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def chat_message(role: str, content: str, timestamp: str = ""):
    """Render a styled chat bubble using upgraded avatars and classes."""
    if role == "user":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; margin:0.8rem 0;" class="animate-in">
          <div style="display:flex; gap:0.6rem; align-items:flex-end; max-width:80%;">
            <div>
              <div class="chat-bubble-user">{content}</div>
              {"<div class='chat-timestamp' style='text-align:right;'>" + timestamp + "</div>" if timestamp else ""}
            </div>
            <div class="chat-avatar" style="background:#E2E8F0; color:#475569;">👤</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; margin:0.8rem 0;" class="animate-in">
          <div style="display:flex; gap:0.6rem; align-items:flex-start; max-width:85%;">
            <div class="chat-avatar" style="background:linear-gradient(135deg,#8B5CF6,#3B82F6); color:white;">🤖</div>
            <div>
              <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:4px;">
                <span style="font-size:0.75rem; font-weight:700; color:#8B5CF6; letter-spacing:0.02em;">NayePankh AI Mentor</span>
              </div>
              <div class="chat-bubble-assistant">{content}</div>
              {"<div class='chat-timestamp'>" + timestamp + "</div>" if timestamp else ""}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)


def feature_card(icon: str, title: str, description: str, color: str = "#3B82F6"):
    """Render a feature highlight card for the home page."""
    st.markdown(f"""
    <div class="np-card animate-in" style="height:100%; display:flex; flex-direction:column;">
      <div style="width:48px; height:48px; border-radius:12px; display:flex; align-items:center; justify-content:center;
                  font-size:1.5rem; margin-bottom:1rem; background:{color}0F; border:1px solid {color}2A; color:{color};">
        {icon}
      </div>
      <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.1rem; color:#0F172A; margin-bottom:0.5rem;">{title}</div>
      <div style="font-size:0.88rem; color:#64748B; line-height:1.6; flex-grow:1;">{description}</div>
    </div>
    """, unsafe_allow_html=True)


def divider():
    st.markdown('<div class="np-divider"></div>', unsafe_allow_html=True)


def profile_summary_card(profile: dict):
    """Render a compact student profile summary card with upgraded style."""
    name    = profile.get("name", "Student")
    degree  = profile.get("degree", "")
    branch  = profile.get("branch", "")
    year    = profile.get("year", "")
    goal    = profile.get("career_goal", "")
    skills  = profile.get("skills", "")

    initials = "".join(w[0].upper() for w in name.split()[:2]) if name else "S"

    st.markdown(f"""
    <div class="np-card np-card-glow-blue animate-in">
      <div style="display:flex; align-items:center; gap:1.25rem; margin-bottom:1.25rem;">
        <div style="width:64px; height:64px; border-radius:50%;
                    background:linear-gradient(135deg,#8B5CF6,#3B82F6);
                    display:flex; align-items:center; justify-content:center;
                    font-family:'Space Grotesk', sans-serif; font-size:1.5rem; font-weight:700; color:white;
                    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.2); flex-shrink:0;">
          {initials}
        </div>
        <div>
          <div style="font-family:'Space Grotesk', sans-serif; font-size:1.2rem; font-weight:700; color:#0F172A;">{name}</div>
          <div style="font-size:0.85rem; color:#64748B; font-weight:500;">{degree} · {branch}</div>
          <div style="font-size:0.8rem; color:#3B82F6; font-weight:600; margin-top:2px;">{year}</div>
        </div>
      </div>
      <div style="background:rgba(226, 232, 240, 0.3); border-radius:10px; padding:0.75rem 1rem;">
        <div style="font-size:0.88rem; color:#475569; margin-bottom:0.4rem;">
          <strong style="color:#0F172A; font-weight:700;">🎯 Goal:</strong> {goal or "Not specified"}
        </div>
        <div style="font-size:0.88rem; color:#475569;">
          <strong style="color:#0F172A; font-weight:700;">🛠 Skills:</strong> {skills or "Not listed"}
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def step_badge(number: int, label: str, done: bool = False):
    """Render a numbered step badge with modernized icons."""
    color = "#10B981" if done else "#3B82F6"
    icon  = "✓" if done else str(number)
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.75rem; padding:0.6rem 0;" class="animate-in">
      <div style="width:30px; height:30px; border-radius:50%; background:{color};
                  color:white; font-family:'Space Grotesk', sans-serif; font-size:0.85rem; font-weight:700;
                  display:flex; align-items:center; justify-content:center; flex-shrink:0;
                  box-shadow: 0 3px 8px {color}3A;">
        {icon}
      </div>
      <span style="font-size:0.92rem; font-weight:600; color:{'#10B981' if done else '#0F172A'};
                   text-decoration:{'line-through' if done else 'none'}; opacity:{'0.7' if done else '1'};">
        {label}
      </span>
    </div>
    """, unsafe_allow_html=True)


def loading_spinner(message: str = "Processing...", size: str = "medium"):
    """Render a professional loading spinner with custom message."""
    spinner_html = f"""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                padding:3rem 2rem; gap:1.5rem;">
      <div style="width:50px; height:50px; border:4px solid rgba(59,130,246,0.1);
                  border-top:4px solid #3B82F6; border-radius:50%;
                  animation:spin 1s linear infinite;"></div>
      <div style="font-size:0.95rem; font-weight:600; color:#64748B;">{message}</div>
    </div>
    <style>
    @keyframes spin {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(360deg); }}
    }}
    </style>
    """
    st.markdown(spinner_html, unsafe_allow_html=True)


def success_notification(message: str, icon: str = "✓"):
    """Render a professional success notification."""
    st.markdown(f"""
    <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.2);
                border-left:4px solid #10B981; border-radius:12px; padding:1rem 1.25rem;
                display:flex; align-items:center; gap:0.75rem; margin:1rem 0;" class="animate-in">
      <div style="width:32px; height:32px; background:#10B981; border-radius:50%;
                  display:flex; align-items:center; justify-content:center; color:white; font-size:1.1rem;">
        {icon}
      </div>
      <div style="font-size:0.92rem; font-weight:600; color:#065F46; flex:1;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def error_notification(message: str, icon: str = "⚠"):
    """Render a professional error notification."""
    st.markdown(f"""
    <div style="background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.2);
                border-left:4px solid #EF4444; border-radius:12px; padding:1rem 1.25rem;
                display:flex; align-items:center; gap:0.75rem; margin:1rem 0;" class="animate-in">
      <div style="width:32px; height:32px; background:#EF4444; border-radius:50%;
                  display:flex; align-items:center; justify-content:center; color:white; font-size:1.1rem;">
        {icon}
      </div>
      <div style="font-size:0.92rem; font-weight:600; color:#991B1B; flex:1;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def professional_footer():
    """Render a professional footer for the application."""
    st.markdown("""
    <div class="np-footer">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1.5rem;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
          <div style="font-size:1.8rem;">🕊️</div>
          <div>
            <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.1rem; color:#FFFFFF;">
              NayePankh Career Mentor
            </div>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:2px;">
              AI Career Mentor Platform
            </div>
          </div>
        </div>
        <div style="display:flex; gap:2rem; font-size:0.85rem; color:#94A3B8;">
          <div style="display:flex; flex-direction:column; gap:0.5rem;">
            <div style="font-weight:600; color:#E2E8F0; margin-bottom:0.25rem;">Platform</div>
            <div style="opacity:0.8;">Career Analysis</div>
            <div style="opacity:0.8;">Skill Assessment</div>
            <div style="opacity:0.8;">Learning Paths</div>
          </div>
          <div style="display:flex; flex-direction:column; gap:0.5rem;">
            <div style="font-weight:600; color:#E2E8F0; margin-bottom:0.25rem;">About</div>
            <div style="opacity:0.8;">NayePankh Foundation</div>
            <div style="opacity:0.8;">Our Mission</div>
            <div style="opacity:0.8;">Contact Us</div>
          </div>
        </div>
      </div>
      <div style="margin-top:2rem; padding-top:1.5rem; border-top:1px solid rgba(255,255,255,0.1);
                  display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;">
        <div style="font-size:0.8rem; color:#64748B;">
          © 2026 NayePankh Foundation. All rights reserved.
        </div>
        <div style="font-size:0.8rem; color:#64748B;">
          Built for NayePankh Foundation · Developed by Mayank Mishra
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
