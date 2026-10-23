"""
Notification Service for WhatsApp and SMS delivery.
Supports Twilio API integration for automated SMS/WhatsApp delivery,
as well as instant WhatsApp Click-to-Chat direct links (wa.me) for zero-setup instant messaging.
"""

import os
import urllib.parse
from typing import Dict, Any, Optional
from app.config import settings

# Global notification log for history & debugging in the web app
NOTIFICATION_LOGS = []

def send_notification(
    phone_number: str,
    channel: str,  # 'whatsapp' or 'sms'
    photographer_name: str,
    category: str,
    download_url: str,
    custom_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Sends or prepares a notification via WhatsApp or SMS.
    """
    clean_phone = phone_number.strip().replace(" ", "").replace("-", "")
    if not clean_phone.startswith("+"):
        # Default prefix + if not present
        clean_phone = "+" + clean_phone

    channel = channel.lower()
    
    # Compose message text
    if not custom_message:
        message_body = (
            f"✨ Masterpiece Photo Enhancer ✨\n\n"
            f"Your photo has been professionally enhanced!\n"
            f"📸 Style: {photographer_name}\n"
            f"🎨 Context: {category}\n\n"
            f"View & download your high-res masterpiece here:\n"
            f"{download_url}\n\n"
            f"— Created with Masterpiece AI"
        )
    else:
        message_body = custom_message

    result = {
        "success": False,
        "channel": channel,
        "phone_number": clean_phone,
        "message": message_body,
        "method_used": "",
        "direct_link": None,
        "error": None
    }

    # Generate direct WhatsApp Click-to-Chat link
    encoded_text = urllib.parse.quote(message_body)
    phone_digits = clean_phone.replace("+", "")
    whatsapp_direct_url = f"https://api.whatsapp.com/send?phone={phone_digits}&text={encoded_text}"
    result["direct_link"] = whatsapp_direct_url if channel == "whatsapp" else f"sms:{clean_phone}?body={encoded_text}"

    # Check if Twilio is configured
    account_sid = os.getenv("TWILIO_ACCOUNT_SID") or settings.twilio_account_sid
    auth_token = os.getenv("TWILIO_AUTH_TOKEN") or settings.twilio_auth_token

    if account_sid and auth_token and not account_sid.startswith("your_"):
        try:
            from twilio.rest import Client
            client = Client(account_sid, auth_token)

            if channel == "whatsapp":
                from_num = os.getenv("TWILIO_WHATSAPP_NUMBER") or settings.twilio_whatsapp_number or "whatsapp:+14155238886"
                if not from_num.startswith("whatsapp:"):
                    from_num = f"whatsapp:{from_num}"
                to_num = f"whatsapp:{clean_phone}"

                msg = client.messages.create(
                    body=message_body,
                    from_=from_num,
                    to=to_num
                )
                result["success"] = True
                result["method_used"] = "Twilio WhatsApp API"
                result["twilio_sid"] = msg.sid
            else:  # SMS
                from_num = os.getenv("TWILIO_PHONE_NUMBER") or settings.twilio_phone_number
                msg = client.messages.create(
                    body=message_body,
                    from_=from_num,
                    to=clean_phone
                )
                result["success"] = True
                result["method_used"] = "Twilio SMS API"
                result["twilio_sid"] = msg.sid

        except Exception as e:
            result["error"] = str(e)
            result["success"] = False
            result["method_used"] = "Twilio (Failed, fallback link provided)"
    else:
        # Twilio credentials not provided: Provide instant direct link & simulated dispatch
        result["success"] = True
        result["method_used"] = "Direct Link / Instant Dispatch (Twilio credentials not configured)"

    NOTIFICATION_LOGS.append(result)
    return result

def get_notification_logs():
    return NOTIFICATION_LOGS[-20:]
