import urllib.request
import urllib.parse
import os
from config import BASE_DIR, load_env

load_env()

WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "")  # In international format: e.g. 919876543210 (without +)
CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY", "")

def send_whatsapp_message(text: str) -> bool:
    """Send a message to your personal WhatsApp using CallMeBot."""
    phone = os.getenv("WHATSAPP_PHONE", WHATSAPP_PHONE)
    api_key = os.getenv("CALLMEBOT_API_KEY", CALLMEBOT_API_KEY)
    
    if not phone or not api_key:
        print("⚠️ WhatsApp delivery skipped: WHATSAPP_PHONE or CALLMEBOT_API_KEY not set in .env")
        return False

    # Clean phone number (remove +, spaces, dashes)
    clean_phone = phone.replace("+", "").replace(" ", "").replace("-", "")
    
    # URL encode the message
    encoded_text = urllib.parse.quote(text)
    url = f"https://api.callmebot.com/whatsapp.php?phone={clean_phone}&text={encoded_text}&apikey={api_key}"
    
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
            if "Message queued" in content or "success" in content.lower():
                print("✅ WhatsApp message sent successfully!")
                return True
            else:
                print(f"CallMeBot response: {content}")
                return True
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")
        return False
