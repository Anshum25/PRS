import os
import sys
from datetime import datetime
from pathlib import Path

# Add current directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config
from trend_fetcher import get_current_tech_trends
from generator import generate_post_recommendations

def check_or_prompt_api_key():
    """Ensure Gemini API key is available or prompt user to save one."""
    if not config.GEMINI_API_KEY:
        print("\n" + "="*60)
        print("🔑 GEMINI API KEY REQUIRED")
        print("="*60)
        print("To generate custom AI drafts in your tone, you need a free Gemini API key.")
        print("You can get one in 10 seconds at: https://aistudio.google.com/app/apikey")
        print("="*60)
        user_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
        if user_key:
            env_file = BASE_DIR / ".env"
            with open(env_file, "a", encoding="utf-8") as f:
                f.write(f"\nGEMINI_API_KEY={user_key}\n")
            config.GEMINI_API_KEY = user_key
            print("✅ Key saved to post_recommendation_system/.env!\n")
        else:
            print("⚠️ Proceeding without API key. Some generation features will be disabled.\n")

def save_drafts_to_markdown(topic: str, content: str):
    """Save generated drafts to drafts.md with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draft_entry = f"""
## 📅 Drafts Generated: {timestamp}
**Source / Topic**: {topic}

{content}

---
"""
    with open(config.DRAFTS_FILE, "a", encoding="utf-8") as f:
        f.write(draft_entry)
    print(f"\n💾 Drafts saved to: {config.DRAFTS_FILE}")

def run_trend_mode():
    """Fetch live trends, allow selection, and generate tailored posts."""
    print("\n🔍 Fetching latest tech & AI trends from Hacker News, Reddit, and Google News...")
    trends = get_current_tech_trends()
    
    print("\n" + "="*65)
    print("🔥 TODAY'S TOP TECH & AI TRENDS")
    print("="*65)
    for idx, item in enumerate(trends[:8], 1):
        source = item.get("source", "Web")
        title = item.get("title", "")
        print(f"[{idx}] ({source}) {title}")
    print("="*65)
    
    choice = input("\nSelect a trend number (1-8) to generate posts for, or 'C' for custom topic: ").strip()
    
    if choice.upper() == 'C':
        topic = input("\nEnter your topic, bug, or thought: ").strip()
        context = ""
    else:
        try:
            selected_idx = int(choice) - 1
            if 0 <= selected_idx < len(trends):
                topic = trends[selected_idx]["title"]
                context = f"Source: {trends[selected_idx].get('source', '')}"
            else:
                print("Invalid choice, defaulting to top trend.")
                topic = trends[0]["title"]
                context = f"Source: {trends[0].get('source', '')}"
        except ValueError:
            print("Invalid input, defaulting to top trend.")
            topic = trends[0]["title"]
            context = f"Source: {trends[0].get('source', '')}"

    print(f"\n✍️ Generating 4 @TheAnshumDev-style drafts for: \"{topic}\"...\n")
    try:
        drafts = generate_post_recommendations(topic, context)
        print(drafts)
        save_drafts_to_markdown(topic, drafts)
    except Exception as e:
        print(f"❌ Error generating posts: {e}")

def run_custom_thought_mode():
    """Quick generation for random thoughts, debugging stories, or reflections."""
    print("\n💡 CUSTOM THOUGHT / DEV STORY GENERATOR")
    print("Tell me what you're working on or thinking today.")
    print("Examples: 'Debugging an XGBoost model with class imbalance', 'Docker memory leak', 'Feeling tired of people arguing about AGI'")
    thought = input("\nYour thought: ").strip()
    if not thought:
        print("No thought provided.")
        return
        
    print(f"\n✍️ Generating polished drafts for your profile...\n")
    try:
        drafts = generate_post_recommendations(thought)
        print(drafts)
        save_drafts_to_markdown(thought, drafts)
    except Exception as e:
        print(f"❌ Error generating posts: {e}")

def main_menu():
    print("\n" + "="*65)
    print("🚀 POST RECOMMENDATION SYSTEM (@TheAnshumDev Voice Engine)")
    print("="*65)
    print("1. Scan Live Tech & AI Trends (HackerNews / Reddit / News)")
    print("2. Turn a Raw Thought / Coding Story into Polished Posts")
    print("3. View Saved Drafts (drafts.md)")
    print("4. Configure Gemini API Key")
    print("5. Exit")
    print("="*65)
    
    choice = input("Enter option (1-5): ").strip()
    
    if choice == "1":
        check_or_prompt_api_key()
        run_trend_mode()
    elif choice == "2":
        check_or_prompt_api_key()
        run_custom_thought_mode()
    elif choice == "3":
        if config.DRAFTS_FILE.exists():
            print(f"\n📄 Reading {config.DRAFTS_FILE}:\n")
            with open(config.DRAFTS_FILE, "r", encoding="utf-8") as f:
                print(f.read())
        else:
            print("\nNo saved drafts yet. Generate some first!")
    elif choice == "4":
        config.GEMINI_API_KEY = ""
        check_or_prompt_api_key()
    elif choice == "5":
        print("\nHave a great day posting! 👋")
        sys.exit(0)
    else:
        print("Invalid option. Please choose 1-5.")

if __name__ == "__main__":
    while True:
        try:
            main_menu()
            cont = input("\nPress Enter to return to menu (or 'q' to quit): ").strip()
            if cont.lower() == 'q':
                break
        except KeyboardInterrupt:
            print("\nExiting. Keep building! 🚀")
            break
