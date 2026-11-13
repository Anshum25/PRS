import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config
from trend_fetcher import get_current_tech_trends
from generator import generate_post_recommendations
from telegram_sender import send_telegram_message
from whatsapp_sender import send_whatsapp_message

def run_daily_automation():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Running Daily Content Job for @TheAnshumDev...")
    
    # 1. Fetch live trends
    trends = get_current_tech_trends()
    if not trends:
        print("No trends found, using fallback topic.")
        top_trend = "The reality of building an end-to-end RAG architecture with real validation gates"
        source = "ML Systems"
    else:
        top_trend = trends[0]["title"]
        source = trends[0].get("source", "Live Trend")
    
    print(f"Top Trend Selected: [{source}] {top_trend}")
    
    # 2. Generate drafts
    drafts = generate_post_recommendations(top_trend, f"Source: {source}")
    
    # 3. Save to drafts.md
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draft_entry = f"\n## 📅 Automated Daily Drafts: {timestamp}\n**Topic**: [{source}] {top_trend}\n\n{drafts}\n\n---\n"
    with open(config.DRAFTS_FILE, "a", encoding="utf-8") as f:
        f.write(draft_entry)
    print(f"Saved to {config.DRAFTS_FILE}")

    # 4. Format Message
    message = f"""🔥 *Today's X Posts for @TheAnshumDev*
📅 {datetime.now().strftime('%d %b %Y')}
📌 *Trend*: {top_trend}

{drafts}

👉 *Pick one, make any quick tweak, and post on X!*
"""
    
    # 5. Send via Telegram first (recommended & instant)
    telegram_ok = send_telegram_message(message)
    if not telegram_ok:
        print("Telegram not delivered, checking WhatsApp...")
        send_whatsapp_message(message)
        
    print("Daily job complete! 🎉")

if __name__ == "__main__":
    run_daily_automation()
