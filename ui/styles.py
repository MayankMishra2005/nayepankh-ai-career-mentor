# =============================================================================
# ui/styles.py
# Custom CSS for the NayePankh Career Mentor application.
# Premium UI design with glassmorphism, modern gradients, and smooth animations.
# =============================================================================

MAIN_CSS = """
<style>
/* ── Google Fonts ───────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

/* ── Root Variables ─────────────────────────────────────────── */
:root {
  --primary:      #3B82F6;
  --primary-glow: rgba(59, 130, 246, 0.15);
  --secondary:    #8B5CF6;
  --secondary-glow: rgba(139, 92, 246, 0.15);
  --accent:       #10B981;
  --accent-glow:  rgba(16, 185, 129, 0.15);
  --warning:      #F59E0B;
  --danger:       #EF4444;
  --bg:           #F8FAFC;
  --card:         rgba(255, 255, 255, 0.85);
  --text:         #0F172A;
  --muted:        #64748B;
  --border:       rgba(226, 232, 240, 0.8);
  --radius:       16px;
  --shadow:       0 10px 30px -10px rgba(59, 130, 246, 0.08);
  --shadow-lg:    0 20px 40px -15px rgba(139, 92, 246, 0.18);
}

/* ── Base ───────────────────────────────────────────────────── */
html, body {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  background-color: var(--bg) !important;
  scroll-behavior: smooth;
}

/* Main content text — avoid blanket [class*="css"] overrides that break widgets */
.main, .main p, .main span, .main li, .main h1, .main h2, .main h3, .main h4 {
  color: var(--text);
}

/* ── Streamlit chrome ────────────────────────────────────────── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }

/* CRITICAL: keep header/toolbar visible so sidebar can always be reopened */
[data-testid="stHeader"] {
  visibility: visible !important;
  background: rgba(248, 250, 252, 0.95) !important;
  border-bottom: 1px solid var(--border) !important;
  z-index: 999 !important;
}
[data-testid="stToolbar"],
[data-testid="stHeader"] button,
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[kind="header"],
button[kind="headerNoPadding"] {
  visibility: visible !important;
}
.stDeployButton { display: none !important; }

/* Floating hint when sidebar is collapsed */
[data-testid="collapsedControl"] {
  color: var(--primary) !important;
  background: white !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  box-shadow: var(--shadow) !important;
}

/* ── Professional Footer ─────────────────────────────────────── */
.np-footer {
  background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem 3rem;
  margin-top: 3rem;
  border-radius: 16px 16px 0 0;
}

/* ── Glassmorphism Cards ─────────────────────────────────────── */
.np-card {
  background: var(--card);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}

.np-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

/* ── Hero Section ─────────────────────────────────────────────── */
.np-hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: var(--radius);
  padding: 2.5rem 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
}

.hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: white;
  line-height: 1.2;
  margin-bottom: 0.75rem;
}

.hero-sub {
  font-size: 1rem;
  color: rgba(255,255,255,0.9);
  line-height: 1.6;
  max-width: 600px;
}

/* ── Animations ─────────────────────────────────────────────── */
.animate-in {
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ── Sidebar Styling ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%) !important;
  border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Sidebar text — scoped, not wildcard (avoids breaking buttons/inputs) */
[data-testid="stSidebar"] .np-logo-text,
[data-testid="stSidebar"] .np-logo-sub,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stRadio label p,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span {
  color: #E2E8F0 !important;
}

.np-logo-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.np-logo-sub {
  font-size: 0.8rem;
  color: #94A3B8;
  font-weight: 500;
}

/* ── Radio Navigation ────────────────────────────────────────── */
[data-testid="stSidebar"] .stRadio label {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 10px 12px !important;
  margin: 3px 0 !important;
  transition: all 0.2s ease;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
  background: rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 246, 0.3);
  transform: translateX(4px);
}

[data-testid="stSidebar"] .stRadio input:checked + div {
  background: linear-gradient(90deg, rgba(99, 102, 241, 0.3), rgba(139, 92, 246, 0.2)) !important;
  border-left: 3px solid #3B82F6 !important;
  border-radius: 0 8px 8px 0 !important;
}

/* ── Buttons ─────────────────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
  border: none !important;
  border-radius: 8px !important;
  padding: 10px 20px !important;
  font-weight: 600 !important;
  transition: all 0.2s ease !important;
}

.stButton > button:hover {
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}

/* ── Input Fields ─────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
  background: #FFFFFF !important;
  border: 1.5px solid #CBD5E1 !important;
  border-radius: 10px !important;
  color: #0F172A !important;
  -webkit-text-fill-color: #0F172A !important;
  padding: 10px 14px !important;
  font-size: 0.95rem !important;
  min-height: 44px !important;
  transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder,
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
  color: #94A3B8 !important;
  opacity: 1 !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: #3B82F6 !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
  outline: none !important;
  background: #FFFFFF !important;
}

/* Form labels — must be dark and readable on light background */
.main [data-testid="stWidgetLabel"] p,
.main [data-testid="stWidgetLabel"] label,
.main .stTextInput label,
.main .stTextArea label,
.main .stSelectbox label,
.main .stForm label p {
  color: #0F172A !important;
  font-weight: 600 !important;
  font-size: 0.92rem !important;
}

/* Help text under fields */
.main [data-testid="stTooltipIcon"],
.main .stCaption,
.main small {
  color: #64748B !important;
}

/* Selectbox dropdown value text */
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
  color: #0F172A !important;
}

/* Form container */
[data-testid="stForm"] {
  background: rgba(255, 255, 255, 0.95) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1.5rem 1.75rem !important;
  box-shadow: var(--shadow) !important;
}

/* Chat input at bottom */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input {
  background: #FFFFFF !important;
  color: #0F172A !important;
  border: 1.5px solid #CBD5E1 !important;
}

/* ── Mobile Responsiveness ───────────────────────────────────── */
@media (max-width: 768px) {
  .np-footer {
    padding: 1.5rem 1rem;
  }
  
  .np-hero {
    padding: 2rem 1rem !important;
  }
  
  .hero-title {
    font-size: 1.8rem !important;
  }
  
  .hero-sub {
    font-size: 0.9rem !important;
  }
  
  [data-testid="stSidebar"] {
    width: 100% !important;
  }
}

/* ── Warning Box ─────────────────────────────────────────────── */
.np-warning-box {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(239, 68, 68, 0.1));
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 12px;
  padding: 1rem 1.25rem;
}

/* ── Section Headers ─────────────────────────────────────────── */
.np-section-header {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: #1E293B;
  margin-bottom: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* ── Feature Cards ───────────────────────────────────────────── */
.feature-icon {
  font-size: 2rem;
  margin-bottom: 0.75rem;
}

/* ── Scrollbar ──────────────────────────────────────────────── */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* ── Success/Error Messages ─────────────────────────────────── */
.stSuccess {
  background: rgba(16, 185, 129, 0.1) !important;
  border: 1px solid rgba(16, 185, 129, 0.3) !important;
  border-radius: 8px !important;
}

.stError {
  background: rgba(239, 68, 68, 0.1) !important;
  border: 1px solid rgba(239, 68, 68, 0.3) !important;
  border-radius: 8px !important;
}

/* ── Loading Spinner ─────────────────────────────────────────── */
.stSpinner {
  color: var(--primary) !important;
}

/* ── Metrics and Stats ─────────────────────────────────────── */
.stMetric {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  padding: 1rem !important;
}

/* ── Expander ─────────────────────────────────────────────────── */
.stExpander {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}

/* ── Tabs ───────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}

.stTabs [data-baseweb="tab"] {
  color: var(--muted) !important;
  font-weight: 500 !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%) !important;
  color: white !important;
  border-radius: 6px !important;
}

/* ── Progress Bar ───────────────────────────────────────────── */
.stProgressbar .stProgressbar-value {
  background: linear-gradient(90deg, #3B82F6, #8B5CF6) !important;
  border-radius: 99px !important;
}

/* ── Dataframe ─────────────────────────────────────────────── */
.stDataFrame {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}

.stDataFrame table {
  color: #0F172A !important;
}

/* ── Info/Success/Error Icons ─────────────────────────────────── */
.stAlert {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: #0F172A !important;
}

/* ── Main Content Area ──────────────────────────────────────── */
.main .block-container {
  padding: 2.5rem 3.5rem !important;
  max-width: 1300px !important;
}

/* ── Headings ───────────────────────────────────────────────── */
h1 { font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; color: var(--text) !important; letter-spacing: -0.02em; }
h2 { font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; color: var(--text) !important; letter-spacing: -0.01em; }
h3 { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; color: var(--text) !important; }

/* ── Glass Card Component ───────────────────────────────────── */
.np-card {
  background: var(--card);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  padding: 1.75rem;
  box-shadow: var(--shadow);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
}
.np-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
  border-color: rgba(139, 92, 246, 0.3);
}

/* ── Glowing Card Border Effect ────────────────────────────── */
.np-card-glow-blue::before {
  content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
}
.np-card-glow-green::before {
  content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px;
  background: linear-gradient(90deg, var(--accent), #34D399);
}
.np-card-glow-purple::before {
  content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px;
  background: linear-gradient(90deg, var(--secondary), #F43F5E);
}

/* ── Premium Metric Card ────────────────────────────────────── */
.np-metric {
  background: var(--card);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  padding: 1.5rem;
  box-shadow: var(--shadow);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
}
.np-metric:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-3px);
  border-color: rgba(139, 92, 246, 0.25);
}
.np-metric .metric-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 0.8rem;
  background: rgba(139, 92, 246, 0.08);
  border: 1px solid rgba(139, 92, 246, 0.15);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.05);
}
.np-metric .metric-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 0.4rem;
  background: linear-gradient(135deg, var(--text) 30%, var(--muted) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.np-metric .metric-label {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.np-metric .metric-sub {
  font-size: 0.8rem;
  color: var(--muted);
  margin-top: 0.25rem;
  opacity: 0.8;
}

/* ── Hero Banner ─────────────────────────────────────────────── */
.np-hero {
  background: linear-gradient(135deg, #090D1A 0%, #15102A 50%, #1E112E 100%);
  border-radius: 20px;
  padding: 3.5rem 3rem;
  color: white !important;
  margin-bottom: 2.5rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 40px rgba(9, 13, 26, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
.np-hero::before {
  content: ''; position: absolute; top: -50%; right: -20%; width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, transparent 70%);
  filter: blur(40px);
}
.np-hero::after {
  content: ''; position: absolute; bottom: -40%; left: -10%; width: 400px; height: 400px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.12) 0%, transparent 70%);
  filter: blur(40px);
}
.np-hero h1, .np-hero h2, .np-hero p, .np-hero span { color: white !important; }
.np-hero .hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
  margin-bottom: 1rem;
  background: linear-gradient(90deg, #FFFFFF 30%, #C084FC 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.np-hero .hero-sub {
  font-size: 1.15rem;
  opacity: 0.85;
  max-width: 650px;
  line-height: 1.6;
}

/* ── Section Header ──────────────────────────────────────────── */
.np-section-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin: 2.2rem 0 1.2rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}
.np-section-header .section-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 2px 8px var(--primary-glow));
}
.np-section-header .section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
  letter-spacing: -0.01em;
}

/* ── Divider ─────────────────────────────────────────────────── */
.np-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.15), transparent);
  margin: 2rem 0;
}

/* ── Boxes ───────────────────────────────────────────────────── */
.np-info-box {
  background: rgba(59, 130, 246, 0.05);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-left: 4px solid var(--primary);
  border-radius: 12px;
  padding: 1.1rem 1.4rem;
  font-size: 0.92rem;
  color: #1E40AF;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.np-warning-box {
  background: rgba(245, 158, 11, 0.05);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-left: 4px solid var(--warning);
  border-radius: 12px;
  padding: 1.1rem 1.4rem;
  font-size: 0.92rem;
  color: #92400E;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.np-success-box {
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-left: 4px solid var(--accent);
  border-radius: 12px;
  padding: 1.1rem 1.4rem;
  font-size: 0.92rem;
  color: #065F46;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

/* ── Button Overrides ────────────────────────────────────────── */
.stButton > button {
  border-radius: 10px !important;
  font-weight: 600 !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
  border: 1px solid rgba(139, 92, 246, 0.2) !important;
  padding: 0.6rem 1.2rem !important;
  height: auto !important;
  font-size: 0.9rem !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, var(--secondary), var(--primary)) !important;
  color: white !important;
  border: none !important;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.25) !important;
}
.stButton > button[kind="primary"]:hover {
  box-shadow: 0 8px 25px rgba(139, 92, 246, 0.45) !important;
  transform: translateY(-2px) !important;
  color: white !important;
}
.stButton > button:not([kind="primary"]) {
  background: rgba(255, 255, 255, 0.7) !important;
  color: var(--text) !important;
}
.stButton > button:not([kind="primary"]):hover {
  border-color: var(--secondary) !important;
  color: var(--secondary) !important;
  background: rgba(139, 92, 246, 0.05) !important;
  transform: translateY(-1px) !important;
}

/* ── Input Fields (main area) ────────────────────────────────── */
.stTextInput input, .stTextArea textarea {
  border-radius: 10px !important;
  border: 1.5px solid #CBD5E1 !important;
  background-color: #FFFFFF !important;
  font-size: 0.95rem !important;
  color: #0F172A !important;
  -webkit-text-fill-color: #0F172A !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--secondary) !important;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.12) !important;
  background-color: #FFFFFF !important;
}

/* Sidebar buttons — keep readable on dark bg */
[data-testid="stSidebar"] .stButton > button {
  color: #F8FAFC !important;
  background: rgba(255, 255, 255, 0.08) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(99, 102, 241, 0.25) !important;
  border-color: rgba(99, 102, 241, 0.4) !important;
  color: #FFFFFF !important;
}

/* ── Tab Styling ─────────────────────────────────────────────── */
[data-testid="stTabs"] {
  background: transparent !important;
  margin-bottom: 1.5rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: rgba(226, 232, 240, 0.5) !important;
  border-radius: 12px !important;
  padding: 4px !important;
  border: 1px solid var(--border) !important;
  gap: 4px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  font-weight: 600 !important;
  color: var(--muted) !important;
  padding: 8px 16px !important;
  border-radius: 8px !important;
  border-bottom: none !important;
  transition: all 0.25s ease !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--secondary) !important;
  background: rgba(255, 255, 255, 0.5) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  color: white !important;
  background: var(--secondary) !important;
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2) !important;
}

/* ── Expander ────────────────────────────────────────────────── */
[data-testid="stExpander"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  background: var(--card) !important;
  box-shadow: var(--shadow) !important;
  margin-bottom: 1rem !important;
}

/* ── Badge / Tag ─────────────────────────────────────────────── */
.np-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.76rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  margin: 3px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
}
.np-badge-blue   { background: rgba(59, 130, 246, 0.08); color: var(--primary); border: 1px solid rgba(59, 130, 246, 0.2); }
.np-badge-green  { background: rgba(16, 185, 129, 0.08); color: var(--accent); border: 1px solid rgba(16, 185, 129, 0.2); }
.np-badge-purple { background: rgba(139, 92, 246, 0.08); color: var(--secondary); border: 1px solid rgba(139, 92, 246, 0.2); }
.np-badge-amber  { background: rgba(245, 158, 11, 0.08); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.2); }
.np-badge-red    { background: rgba(239, 68, 68, 0.08); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.2); }

/* ── Progress Bar ────────────────────────────────────────────── */
.np-progress-wrap {
  background: rgba(226, 232, 240, 0.6);
  border-radius: 99px;
  height: 10px;
  overflow: hidden;
  margin: 0.5rem 0;
  border: 1px solid rgba(226, 232, 240, 0.8);
}
.np-progress-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Interactive Workflow Visualizer ────────────────────────── */
.flow-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 1.5rem 0;
  margin-bottom: 2rem;
  overflow-x: auto;
  gap: 10px;
}
.flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  min-width: 120px;
  flex: 1;
}
.flow-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  background: white;
  border: 2px solid var(--border);
  box-shadow: var(--shadow);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  z-index: 2;
  cursor: pointer;
}
.flow-step.active .flow-icon-wrap {
  border-color: var(--secondary);
  background: linear-gradient(135deg, var(--secondary), var(--primary));
  box-shadow: 0 0 20px var(--secondary-glow);
  transform: scale(1.15);
  color: white !important;
}
.flow-step.completed .flow-icon-wrap {
  border-color: var(--accent);
  background: rgba(16, 185, 129, 0.1);
  box-shadow: 0 0 15px var(--accent-glow);
}
.flow-step.completed .flow-icon-wrap::after {
  content: '✓';
  position: absolute;
  bottom: 0;
  right: 28px;
  background: var(--accent);
  color: white;
  font-size: 0.65rem;
  font-weight: 800;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid white;
}
.flow-label {
  font-size: 0.76rem;
  font-weight: 700;
  color: var(--muted);
  margin-top: 0.6rem;
  transition: color 0.3s;
}
.flow-step.active .flow-label { color: var(--secondary); }
.flow-step.completed .flow-label { color: var(--text); }

.flow-connector {
  flex-grow: 1;
  height: 3px;
  background: var(--border);
  margin-bottom: 24px;
  position: relative;
  border-radius: 99px;
  z-index: 1;
  min-width: 20px;
}
.flow-connector.active {
  background: linear-gradient(90deg, var(--accent), var(--border));
}
.flow-connector.completed {
  background: var(--accent);
}

/* ── Developer Terminal Console ────────────────────────────── */
.terminal-console {
  background: #0D0E15;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1.2rem 1.5rem;
  font-family: 'Space Grotesk', 'Courier New', Courier, monospace;
  font-size: 0.85rem;
  color: #34D399;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.8), 0 10px 30px rgba(0,0,0,0.15);
  max-height: 250px;
  overflow-y: auto;
}
.terminal-header {
  display: flex;
  gap: 6px;
  margin-bottom: 0.6rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
.terminal-dot { width: 10px; height: 10px; border-radius: 50%; }
.terminal-red    { background: #EF4444; }
.terminal-yellow { background: #F59E0B; }
.terminal-green  { background: #10B981; }

.terminal-line { margin: 2px 0; }
.terminal-timestamp { color: #64748B; margin-right: 8px; }
.terminal-info { color: #3B82F6; }
.terminal-success { color: #10B981; }
.terminal-warning { color: #F59E0B; }
.terminal-error   { color: #EF4444; }
.terminal-red     { color: #EF4444; }
.terminal-blink::after {
  content: '▋';
  animation: blink 1s step-end infinite;
}
@keyframes blink {
  from, to { color: transparent }
  50% { color: #34D399 }
}

/* ── Circular / Ring Progress Indicator ─────────────────────── */
.ring-container {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.ring-svg-wrap {
  position: relative;
  width: 90px;
  height: 90px;
}
.ring-bg {
  fill: none;
  stroke: rgba(226, 232, 240, 0.8);
  stroke-width: 8;
}
.ring-fill {
  fill: none;
  stroke-width: 8;
  stroke-linecap: round;
  transform: rotate(-90deg);
  transform-origin: 50% 50%;
  transition: stroke-dashoffset 1s ease-in-out;
}
.ring-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.4rem;
  font-weight: 700;
}

/* ── Timeline Navigation / Accordion ────────────────────────── */
.timeline-item {
  border-left: 2px solid var(--border);
  padding-left: 1.5rem;
  position: relative;
  padding-bottom: 2rem;
}
.timeline-item:last-child {
  border-left: 2px solid transparent;
}
.timeline-badge {
  position: absolute;
  left: -9px;
  top: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: white;
  border: 2px solid var(--border);
  transition: all 0.3s;
}
.timeline-item.active .timeline-badge {
  border-color: var(--secondary);
  background: var(--secondary);
  box-shadow: 0 0 10px var(--secondary-glow);
}
.timeline-item.completed .timeline-badge {
  border-color: var(--accent);
  background: var(--accent);
}

/* ── Chat Premium Bubbles ────────────────────────────────────── */
.chat-avatar {
  width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0;
}
.chat-bubble-user {
  background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%) !important;
  color: white !important;
  border-radius: 16px 16px 4px 16px !important;
  padding: 1rem 1.3rem !important;
  max-width: 75%;
  margin-left: auto;
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.15) !important;
  font-size: 0.92rem;
  line-height: 1.5;
}
.chat-bubble-assistant {
  background: var(--card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 16px 16px 16px 4px !important;
  padding: 1rem 1.3rem !important;
  max-width: 80%;
  box-shadow: var(--shadow) !important;
  font-size: 0.92rem;
  line-height: 1.5;
}
.chat-timestamp {
  font-size: 0.72rem;
  color: var(--muted);
  margin-top: 4px;
}

/* ── Animations ──────────────────────────────────────────────── */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

@keyframes pulseGlow {
  0%, 100% { box-shadow: 0 0 10px var(--primary-glow); }
  50% { box-shadow: 0 0 20px var(--primary-glow); }
}
.pulse-glow { animation: pulseGlow 2s infinite; }

/* ── Responsive ──────────────────────────────────────────────── */
@media (max-width: 768px) {
  .main .block-container { padding: 1.5rem 1.5rem !important; }
  .np-hero { padding: 2.2rem 1.8rem; }
  .np-hero .hero-title { font-size: 2.2rem; }
}
</style>
"""
