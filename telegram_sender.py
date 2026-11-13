import os
import urllib.request
import urllib.parse
import json
from config import BASE_DIR, load_env

load_env()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9123159926:AAH9486uKAdqfEymvFjSJ72EiZ-6oqAzeGk")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "9131023398")

def get_latest_chat_id(token: str) -> str:
    """Auto-detect chat ID from the last user who messaged or clicked Start on the bot."""
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            results = data.get("result", [])
            if results:
                last_update = results[-1]
                chat = (
                    last_update.get("message", {}).get("chat", {}) or
                    last_update.get("channel_post", {}).get("chat", {}) or
                    last_update.get("my_chat_member", {}).get("chat", {})
                )
                chat_id = str(chat.get("id", ""))
                return chat_id
    except Exception as e:
        print(f"Error fetching chat ID: {e}")
    return ""

def send_telegram_message(text: str) -> bool:
    """Send text message to Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
    chat_id = os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)
    
    if not token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode()).get("ok", False)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        if "can't parse entities" in err.lower():
            payload.pop("parse_mode", None)
            retry_data = json.dumps(payload).encode("utf-8")
            retry_req = urllib.request.Request(url, data=retry_data, headers={"Content-Type": "application/json"}, method="POST")
            try:
                with urllib.request.urlopen(retry_req, timeout=15) as retry_resp:
                    return json.loads(retry_resp.read().decode()).get("ok", False)
            except Exception:
                pass
        return False
    except Exception:
        return False

def send_telegram_photo(image_url: str, caption: str = "") -> bool:
    """Send an image with caption to Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN)
    chat_id = os.getenv("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)
    
    if not token or not chat_id:
        return False

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {
        "chat_id": chat_id,
        "photo": image_url,
        "caption": caption[:1024],  # Telegram max caption length
        "parse_mode": "Markdown"
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode()).get("ok", False)
    except Exception as e:
        print(f"Error sending photo to Telegram: {e}")
        return False
