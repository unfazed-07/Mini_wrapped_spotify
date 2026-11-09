"""
check_ai.py - tests your AI provider (Gemini or Groq) OUTSIDE Streamlit.

Run from the project folder:   python check_ai.py

It uses the same code path as the app, prints how long the request took, and shows
the full error if something fails. Use it to tell apart "my key / network is the
problem" from "the Streamlit app is the problem".
"""

import time
import traceback

import backend

provider = backend.AI_PROVIDER
model = backend.GROQ_MODEL if provider == "groq" else backend.GEMINI_MODEL
print(f"Provider : {provider}")
print(f"Model    : {model}")
print(f"Key var  : {backend.ai_key_name()}")
print(f"Timeout  : {backend.AI_TIMEOUT_SECONDS}s")

if backend.ai_key_name() in backend.missing_config(include_ai=True):
    print(f"\nPROBLEM: {backend.ai_key_name()} is missing or still a placeholder in your .env file.")
    raise SystemExit(1)

artists = [
    {"name": "Arijit Singh", "genres": ["bollywood", "filmi"]},
    {"name": "The Weeknd", "genres": ["canadian contemporary r&b", "pop"]},
    {"name": "Imagine Dragons", "genres": ["modern rock", "pop rock"]},
]
tracks = [
    {"name": "Starboy", "artist": "The Weeknd, Daft Punk"},
    {"name": "Believer", "artist": "Imagine Dragons"},
    {"name": "Tum Hi Ho", "artist": "Arijit Singh"},
]

print("\nCalling the AI with a small sample...")
start = time.perf_counter()
try:
    result = backend.get_ai_analysis_and_recs(artists, tracks)
except Exception:
    print(f"\nFAILED after {time.perf_counter() - start:.1f}s. Full error:\n")
    traceback.print_exc()
    raise SystemExit(1)

print(f"\nOK in {time.perf_counter() - start:.1f}s  ({result.get('meta')})")
print("\nRecommendations:")
for i, song in enumerate(result["recommendations"], 1):
    print(f"  {i}. {song}")
print("\nFirst 300 characters of the roast:\n" + result["roast_and_aura"][:300])
