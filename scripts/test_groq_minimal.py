#!/usr/bin/env python3
"""Minimal Groq connectivity test — run before migrating the app."""
import os
import sys

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

try:
    from groq import Groq
except ImportError:
    print("FAIL: groq package not installed. Run: pip install groq")
    sys.exit(1)

MODEL = "llama-3.3-70b-versatile"
PROMPT = "Say Hello"

api_key = os.getenv("GROQ_API_KEY", "").strip()
if not api_key:
    print("FAIL: GROQ_API_KEY not set in .env")
    sys.exit(1)

print("GROQ_API_KEY configured: yes")
print("Model:", MODEL)
print("Prompt:", PROMPT)

client = Groq(api_key=api_key)
response = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": PROMPT}],
    max_tokens=64,
    temperature=0.7,
)

text = response.choices[0].message.content
print("Status: OK")
print("Response:", text)
