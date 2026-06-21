#!/usr/bin/env python3
"""End-to-end LLM validation — Groq primary, all agent entry points."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from utils.llm_client import call_llm, verify_api_connection, is_ai_error
from utils.groq_client import call_groq
from config.settings import GROQ_MODEL

SAMPLE_PROFILE = {
    "name": "Test Student",
    "degree": "B.Tech / B.E.",
    "branch": "Computer Science & Engineering",
    "year": "3rd Year",
    "skills": "Python, SQL, Git",
    "interests": "Open source",
    "career_goal": "Software Engineer",
    "industry": "Technology / Software",
    "additional_info": "Validation test run",
}

AGENT_TESTS = [
    ("Profile Analyzer", "agents.profile_analyzer", "run_profile_analyzer", (SAMPLE_PROFILE,)),
    ("Career Mentor", "agents.career_mentor", "run_career_mentor", (SAMPLE_PROFILE,)),
    ("Learning Roadmap", "agents.learning_roadmap", "run_learning_roadmap", (SAMPLE_PROFILE, "Software Engineer")),
    ("Project Recommender", "agents.project_recommender", "run_project_recommender", (SAMPLE_PROFILE, "Software Engineer")),
    ("Internship Readiness", "agents.internship_readiness", "run_internship_readiness", (SAMPLE_PROFILE,)),
    ("Motivation", "agents.motivation_guidance", "run_motivation_guidance", (SAMPLE_PROFILE,)),
]


def main():
    print("=== Groq connectivity ===")
    ok, msg = verify_api_connection()
    print(f"verify_api_connection: ok={ok} msg={msg}")
    if not ok:
        print("FAIL: Groq not connected")
        sys.exit(1)

    print("\n=== call_groq: Say Hello ===")
    hello = call_groq("Say Hello")
    print(f"Response: {hello[:200]}")
    if is_ai_error(hello):
        print("FAIL: call_groq returned error")
        sys.exit(1)

    print("\n=== call_llm: Say Hello ===")
    hello2 = call_llm("Say Hello")
    print(f"Response: {hello2[:200]}")
    if is_ai_error(hello2):
        print("FAIL: call_llm returned error")
        sys.exit(1)

    print(f"\n=== Agent smoke tests (model: {GROQ_MODEL}) ===")
    import importlib
    for label, mod_path, fn_name, args in AGENT_TESTS:
        mod = importlib.import_module(mod_path)
        fn = getattr(mod, fn_name)
        print(f"  Running {label}...", end=" ", flush=True)
        try:
            result = fn(*args)
            if isinstance(result, tuple):
                result = result[0]
            if is_ai_error(result):
                print(f"FAIL (error response): {str(result)[:120]}")
                sys.exit(1)
            print(f"OK ({len(str(result))} chars)")
        except Exception as e:
            print(f"FAIL ({e})")
            sys.exit(1)

    print("\n=== Module smoke tests ===")
    from modules.skill_gap import run_skill_gap_analysis
    r = run_skill_gap_analysis(SAMPLE_PROFILE, "Software Engineer", "Technology / Software")
    if is_ai_error(r):
        print(f"FAIL skill_gap: {r[:120]}")
        sys.exit(1)
    print(f"  skill_gap OK ({len(r)} chars)")

    print("\nAll Groq LLM tests passed.")


if __name__ == "__main__":
    main()
