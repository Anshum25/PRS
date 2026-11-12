import os
import urllib.request
import urllib.parse
import base64
import json
from config import BASE_DIR, load_env

load_env()

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+17372508034") # default from sandbox
WHATSAPP_TO = os.getenv("WHATSAPP_PHONE", "") # e.g. 917698895249 or 917778895249

def send_whatsapp_message(text: str) -> bool:
    """Send a WhatsApp message via official Twilio API (zero external dependencies)."""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID", TWILIO_ACCOUNT_SID)
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", TWILIO_AUTH_TOKEN)
    to_phone = os.getenv("WHATSAPP_PHONE", WHATSAPP_TO)
    from_whatsapp = os.getenv("TWILIO_WHATSAPP_FROM", TWILIO_WHATSAPP_FROM)
    
    if not account_sid or not auth_token:
        print("⚠️ Twilio credentials missing: set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN in .env")
        return False
        
    if not to_phone:
        print("⚠️ Target phone missing: set WHATSAPP_PHONE in .env")
        return False

    # Ensure format 'whatsapp:+91...'
    clean_to = to_phone.replace(" ", "").replace("-", "")
    if not clean_to.startswith("+"):
        clean_to = "+" + clean_to
    if not clean_to.startswith("whatsapp:"):
        clean_to = "whatsapp:" + clean_to
        
    if not from_whatsapp.startswith("whatsapp:"):
        from_whatsapp = "whatsapp:" + from_whatsapp

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    
    # Twilio API uses standard form-urlencoded POST
    data = urllib.parse.urlencode({
        "From": from_whatsapp,
        "To": clean_to,
        "Body": text
    }).encode("utf-8")
    
    # HTTP Basic Authentication
    auth_str = f"{account_sid}:{auth_token}"
    b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res_data = json.loads(resp.read().decode())
            print(f"✅ Twilio WhatsApp message sent successfully! SID: {res_data.get('sid', '')}")
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        print(f"❌ Twilio WhatsApp error {e.code}: {error_body}")
        return False
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {e}")
        return False
