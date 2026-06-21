#!/usr/bin/env python3
"""Validate all modules import and core wiring is correct."""
import sys
import importlib

ROOT = __file__.rsplit("/", 1)[0] + "/.."
sys.path.insert(0, ROOT if not ROOT.endswith("/..") else __file__.rsplit("/", 2)[0])

MODULES = [
    "app",
    "config.settings",
    "utils.groq_client",
    "utils.llm_client",
    "utils.gemini_client",
    "utils.memory",
    "utils.helpers",
    "ui.styles",
    "ui.sidebar",
    "ui.components",
    "ui.navigation",
    "agents.profile_analyzer",
    "agents.career_mentor",
    "agents.learning_roadmap",
    "agents.project_recommender",
    "agents.internship_readiness",
    "agents.motivation_guidance",
    "modules.resume_analyzer",
    "modules.linkedin_reviewer",
    "modules.skill_gap",
    "modules.export",
    "page_modules.page_home",
    "page_modules.page_profile",
    "page_modules.page_agents",
    "page_modules.page_resume",
    "page_modules.page_linkedin",
    "page_modules.page_skillgap",
    "page_modules.page_roadmap",
    "page_modules.page_chatbot",
    "page_modules.page_dashboard",
    "page_modules.page_goals",
    "page_modules.page_about",
]

def main():
    failed = []
    for mod in MODULES:
        try:
            importlib.import_module(mod)
            print(f"OK  {mod}")
        except Exception as e:
            print(f"FAIL {mod}: {e}")
            failed.append(mod)
    if failed:
        print(f"\n{len(failed)} module(s) failed")
        sys.exit(1)
    print(f"\nAll {len(MODULES)} modules imported successfully")
    from config.settings import GROQ_MODEL, GROQ_FALLBACK_MODELS
    print(f"Groq model: {GROQ_MODEL}, fallbacks: {GROQ_FALLBACK_MODELS}")

if __name__ == "__main__":
    main()
