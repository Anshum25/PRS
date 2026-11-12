import json
import urllib.request
import urllib.error
from typing import Dict, Any, List
from config import GEMINI_API_KEY, GEMINI_MODEL, PERSONA_PROMPT

def call_gemini_api(prompt: str) -> str:
    """Call the Gemini REST API directly using standard urllib."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Add it in .env or enter it when prompted.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.75,
            "maxOutputTokens": 1000,
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            res_json = json.loads(resp.read().decode())
            candidates = res_json.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            return "No text returned from Gemini."
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API HTTP Error {e.code}: {error_msg}")
    except Exception as e:
        raise RuntimeError(f"Gemini connection failed: {e}")

def generate_post_recommendations(topic_or_trend: str, context: str = "") -> str:
    """Generate 4 tailored post options in @TheAnshumDev's exact tone."""
    
    full_prompt = f"""
{PERSONA_PROMPT}

You are generating post drafts for @TheAnshumDev based on the following trend or topic:
TOPIC/TREND: "{topic_or_trend}"
ADDITIONAL CONTEXT: "{context}"

Generate EXACTLY 4 distinct post drafts in markdown format. Each draft must strictly follow the character rules and voice guidelines:

---
### Option 1: The Witty Anti-Hype Take (Viral / High Retweets)
- Goal: Call out the gap between tech hype and real engineering reality with dry, self-aware developer wit.
- Must be UNDER 280 characters.
- Format with clean line breaks.

### Option 2: The Systems / ML Practitioner Angle (High Bookmarks)
- Goal: Focus on actual substance (e.g. math, evaluation, loss, latency, architecture, trade-offs) rather than surface-level impressions.
- Clean, punchy lines. Under 280-350 characters.

### Option 3: The Honest Learner Grind & Quiet Discipline
- Goal: Reflect on the unglamorous reality of learning, debugging, or building when no one is watching.
- Honest, relatable, zero performative positivity.

### Option 4: The Thought-Provoking Discussion Starter (High Replies)
- Goal: Ask a genuine, grounded question that invites developers and engineers to share their war stories or opinions.
- Short and direct.

---
Provide ONLY the 4 options formatted neatly. Show character count for each.
"""
    
    return call_gemini_api(full_prompt)
