# NayePankh Career Mentor AI Agent 🕊️

<div align="center">

![NayePankh](https://img.shields.io/badge/NayePankh-Foundation-1A56DB?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-FF5A5F?style=for-the-badge&logo=groq&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-059669?style=for-the-badge)

**An AI-powered career guidance platform for students — built for NayePankh Foundation**

[Features](#features) · [Architecture](#multi-agent-architecture) · [Installation](#installation) · [Usage](#usage) 

</div>

---

## 📖 Project Overview

**NayePankh Career Mentor** is a production-grade, multi-agent AI application built with Streamlit and Groq. It empowers students across India to discover ideal career paths, identify skill gaps, receive personalised 6-month learning roadmaps, get project recommendations, analyse their resumes, and receive interview/internship preparation guidance — all through a beautiful, professional dashboard interface.

This tool is part of **NayePankh Foundation's** mission to democratise world-class career counselling for underprivileged and first-generation college students.

---

## 🎯 Problem Statement

Millions of Indian students graduate each year without clear career direction, actionable skill development plans, or access to quality mentorship. Traditional career counselling is expensive, geographically limited, and generic. NayePankh Career Mentor solves this by putting a personalised, AI-powered career advisor in every student's pocket — for free.

---

## ✨ Features

### 🤖 Multi-Agent AI System
- **6 specialised AI agents** each focused on a distinct career intelligence task
- Sequential & individual agent execution with cached outputs
- Context-aware responses using the student's complete profile

### 👤 Student Profile Engine
- Comprehensive profile: degree, branch, year, skills, interests, career goal, industry
- Session-state persistence across all pages
- Profile completeness indicator

### 📄 Resume Analyzer
- PDF upload with dual-engine extraction (pdfplumber + PyPDF2 fallback)
- AI-powered analysis with score out of 100
- Missing section detection, ATS compatibility score
- Actionable improvement suggestions

### 💼 LinkedIn Profile Review
- Paste-based LinkedIn profile analysis
- Headline rewrites, About section improvements
- Skills to add, content strategy suggestions

### 📊 Skill Gap Analysis
- Visual skill comparison between current and target
- Critical / High Priority / Nice-to-Have categorisation
- Learning priority ordering with resources

### 🗺️ 6-Month Learning Roadmap
- Month-by-month goals, topics, and resources
- Certification recommendations
- Downloadable Markdown + full PDF export

### 💬 AI Chatbot
- Context-aware career Q&A using profile + conversation history
- Quick-start suggestion prompts
- Chat history download

### 📈 Dashboard
- Overall completion percentage with progress bar
- Score cards: Resume, Internship Readiness, Career Match, Profile
- Agent status grid + recommended next steps

### 🎯 Goal Tracker & Learning Hub
- Add/complete/delete personal career goals
- 12-item internship readiness checklist
- Curated certification database by industry
- AI-generated internship preparation tips

### 📑 PDF Report Export
- Full multi-page PDF with all agent outputs
- Student profile, scores, roadmap, resume analysis, and more

---

## 🏗️ Multi-Agent Architecture

```
Student Profile
      │
      ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT ORCHESTRATOR                       │
│  (pages/page_agents.py + utils/memory.py)                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Agent 1     │   │  Agent 2     │   │  Agent 3     │
│  Profile     │   │  Career      │   │  Learning    │
│  Analyzer    │   │  Mentor      │   │  Roadmap     │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Agent 4     │   │  Agent 5     │   │  Agent 6     │
│  Project     │   │  Internship  │   │  Motivation  │
│  Recommender │   │  Readiness   │   │  & Guidance  │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                    ┌───────▼───────┐
                    │  Session      │
                    │  Memory Store │
                    └───────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
     Dashboard        Chatbot          PDF Report
```

### Agent Responsibilities

| Agent | Role | Key Output |
|-------|------|------------|
| 🧠 Profile Analyzer | SWOT analysis of background | Strengths, Weaknesses, Opportunities |
| 🎯 Career Mentor | Career path matching | Top 3-5 careers with salary & growth |
| 🗺️ Learning Roadmap | 6-month study plan | Month-by-month goals & resources |
| 🏗️ Project Recommender | Portfolio building | Beginner → Advanced project ideas |
| 💼 Internship Readiness | Job-readiness scoring | Score/100 + 30-day action plan |
| 🌟 Motivation & Guidance | Personalised coaching | Competitive advantages + next steps |

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit 1.35+ | UI framework & interactive widgets |
| AI Engine | Groq (Llama 3.3-70B) | All AI-generated content |
| PDF Read | pdfplumber + PyPDF2 | Resume text extraction |
| PDF Write | fpdf2 | Career report PDF generation |
| Data | Pandas | Data handling & display |
| Config | python-dotenv | Environment variable management |
| Memory | Streamlit Session State | Cross-page state persistence |

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- A free Groq API key ([Get one here](https://console.groq.com/keys))

### Steps

```bash
# 1. Clone or navigate to the project
cd nayepankh-career-mentor

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key 
cp .env.example .env
# Edit .env and add: GROQ_API_KEY=your_key_here

# 5. Run the application
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📋 Usage Guide

### Quick Start (5 minutes)

1. **Enter API Key** — Paste your Groq API key in the sidebar under ⚙️ API Settings
2. **Fill Profile** — Go to 👤 My Profile and complete all required fields
3. **Run AI Agents** — Navigate to 🤖 AI Agents and click "🚀 Run All 6 Agents"
4. **Explore Results** — Browse each agent's output, then visit the 📈 Dashboard
5. **Upload Resume** — Go to 📄 Resume Analyzer and upload your PDF
6. **Export Report** — Visit 🗺️ Career Roadmap and download your full PDF report

### Navigation Guide

| Page | What to Do |
|------|-----------|
| 🏠 Home | Learn about features and the platform |
| 👤 My Profile | Fill your academic and career details |
| 🤖 AI Agents | Run 6 AI agents for full career analysis |
| 📄 Resume Analyzer | Upload PDF resume for scoring & feedback |
| 💼 LinkedIn Review | Paste LinkedIn info for optimisation tips |
| 📊 Skill Gap Analysis | See exactly what skills you're missing |
| 🗺️ Career Roadmap | View/export your 6-month learning plan |
| 💬 AI Chatbot | Ask follow-up questions in natural language |
| 📈 Dashboard | See all scores and progress at a glance |
| 🎯 Goal Tracker | Track goals, certifications, and tips |

---

## 📁 Project Structure

```
nayepankh-career-mentor/
├── app.py                    # Main entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── README.md
│
├── config/
│   └── settings.py           # Constants, prompts, UI config
│
├── agents/                   # AI Agent modules
│   ├── profile_analyzer.py   # Agent 1: SWOT analysis
│   ├── career_mentor.py      # Agent 2: Career recommendations
│   ├── learning_roadmap.py   # Agent 3: 6-month roadmap
│   ├── project_recommender.py # Agent 4: Project ideas
│   ├── internship_readiness.py # Agent 5: Readiness scoring
│   └── motivation_guidance.py  # Agent 6: Motivation
│
├── modules/                  # Feature modules
│   ├── resume_analyzer.py    # PDF extraction + analysis
│   ├── linkedin_reviewer.py  # LinkedIn AI review
│   ├── skill_gap.py          # Skill gap computation
│   └── export.py             # PDF report generation
│
├── page_modules/             # Streamlit page renderers
│   ├── page_home.py
│   ├── page_profile.py
│   ├── page_agents.py
│   ├── page_resume.py
│   ├── page_linkedin.py
│   ├── page_skillgap.py
│   ├── page_roadmap.py
│   ├── page_chatbot.py
│   ├── page_dashboard.py
│   └── page_goals.py
│
├── ui/                       # UI layer
│   ├── styles.py             # Custom CSS
│   ├── components.py         # Reusable UI components
│   └── sidebar.py            # Navigation sidebar
│
└── utils/                    # Utility functions
    ├── groq_client.py        # Groq API wrapper
    ├── memory.py             # Session state manager
    └── helpers.py            # Formatting utilities
```

---

## 🔮 Future Enhancements

- [ ] **Voice Input** — Let students speak their questions to the chatbot
- [ ] **College Email Integration** — Auto-detect college/university from email domain
- [ ] **Interview Simulator** — Mock technical and HR interview practice
- [ ] **Job Board Integration** — Live internship listings from Internshala, LinkedIn
- [ ] **Peer Comparison** — Anonymous benchmarking against peers in same branch
- [ ] **Multi-language Support** — Hindi, Tamil, Telugu, and other regional languages
- [ ] **Mobile App** — React Native wrapper for mobile experience
- [ ] **Mentor Matching** — Connect students with NayePankh volunteer mentors
- [ ] **Progress Analytics** — Weekly/monthly progress reports with charts
- [ ] **College Partnerships** — Bulk deployment for college placement cells

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- **NayePankh Foundation** — For the mission and inspiration
- **Groq** — AI engine powering all agents
- **Streamlit** — For making beautiful data apps accessible
- **The open-source community** — For pdfplumber, fpdf2, and all dependencies

---

<div align="center">

Made with ❤️ for students across India

**MAYANK MISHRA**

</div>
