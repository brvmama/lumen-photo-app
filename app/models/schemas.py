from pydantic import BaseModel
from typing import Optional

class NotificationRequest(BaseModel):
    phone_number: str
    channel: str = "whatsapp"  # 'whatsapp' or 'sms'
    photographer_name: str
    category: str
    download_url: str

class EnhanceRequest(BaseModel):
    filename: str
    photographer_id: Optional[str] = None
    intensity: Optional[float] = 0.85
    phone_number: Optional[str] = None
    notification_channel: Optional[str] = "whatsapp"

class SettingsUpdateRequest(BaseModel):
    twilio_account_sid: Optional[str] = None
    twilio_auth_token: Optional[str] = None
    twilio_phone_number: Optional[str] = None
    twilio_whatsapp_number: Optional[str] = None
