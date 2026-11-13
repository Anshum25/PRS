import os
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config
from trend_fetcher import get_current_tech_trends
from generator import generate_post_recommendations
from telegram_sender import send_telegram_message, send_telegram_photo
from image_generator import generate_weekly_image_url

def is_image_day() -> bool:
    """Return True if today is Sunday (weekday 6) or if explicitly requested via env or arg."""
    if "--with-image" in sys.argv:
        return True
    weekly_day = os.getenv("WEEKLY_IMAGE_DAY", "Sunday").strip().lower()
    today_name = datetime.now().strftime("%A").lower()
    return today_name == weekly_day

def run_daily_automation():
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    include_image = is_image_day()
    print(f"\n[{now_str}] 🚀 Running Daily Content Job for @TheAnshumDev... (Image Mode: {include_image})")
    
    # 1. Fetch live trends
    trends = get_current_tech_trends()
    if not trends:
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

    # 4. If it's the weekly image day, generate and send image first
    if include_image:
        print("🎨 Generating weekly 16:9 tech visual for X...")
        image_url = generate_weekly_image_url(top_trend)
        caption = f"🎨 *Weekly Visual Graphic for @TheAnshumDev*\n📌 *Topic*: {top_trend}\n\nAttach this image to Option 2 on X for 2x-3x higher reach!"
        send_telegram_photo(image_url, caption)

    # 5. Format & send the 4 text post drafts
    message = f"""🔥 *Today's X Posts for @TheAnshumDev*
📅 {datetime.now().strftime('%d %b %Y')}
📌 *Trend*: {top_trend}

{drafts}

👉 *Pick one, make any quick tweak, and post on X!*
"""
    send_telegram_message(message)
    print("Daily job complete! 🎉")

if __name__ == "__main__":
    run_daily_automation()
