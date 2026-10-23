import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseModel):
    app_name: str = "Masterpiece Photo Enhancer"
    app_version: str = "1.0.0"
    host: str = "127.0.0.1"
    port: int = 8000
    base_url: str = "http://localhost:8000"

    # Twilio Configuration for WhatsApp & SMS
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")          # E.g. "+1234567890" for SMS
    twilio_whatsapp_number: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "")  # E.g. "whatsapp:+14155238886" (Twilio sandbox)

    # Optional Gemini API Key for deep artistic critique
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
