import os
import uuid
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from app.config import settings, UPLOAD_DIR, STATIC_DIR
from app.services.classifier import analyze_photo_context
from app.services.photographer_catalog import (
    get_all_photographers,
    get_photographer,
    get_default_photographer_for_category
)
from app.services.photo_enhancer import enhance_photo
from app.services.notifier import send_notification, get_notification_logs
from app.models.schemas import NotificationRequest, EnhanceRequest, SettingsUpdateRequest

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Professional photo enhancement web app referencing acclaimed master photographers."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    index_file = Path(__file__).resolve().parent / "templates" / "index.html"
    if not index_file.exists():
        raise HTTPException(status_code=404, detail="Index template not found")
    with open(index_file, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.post("/api/upload")
async def upload_photo(file: UploadFile = File(...)):
    """
    Accepts an uploaded image, saves it, performs context detection,
    and returns the matched master photographer.
    """
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
    ext = Path(file.filename).suffix.lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported format '{ext}'. Please upload JPG, PNG, WEBP, or TIFF.")

    file_id = str(uuid.uuid4())[:8]
    filename = f"original_{file_id}{ext}"
    file_path = UPLOAD_DIR / filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Open and process image: handle phone orientation (EXIF) and scale down if huge
        with Image.open(file_path) as raw_img:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(raw_img) or raw_img
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # If photo from Pixel/iPhone is huge (e.g. 12MP to 50MP), scale to max 2400px (2K HD)
            # This prevents 512MB RAM crash on Render Free Tier while keeping print-grade sharpness
            max_dim = 2400
            if max(img.size) > max_dim:
                scale = max_dim / max(img.size)
                new_size = (int(img.width * scale), int(img.height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save optimized original image
            img.save(file_path, quality=94, optimize=True)
            width, height = img.size
            context_analysis = analyze_photo_context(img)

        # Match default acclaimed photographer for this category
        detected_category = context_analysis["category"]
        matched_photographer = get_default_photographer_for_category(detected_category)

        return {
            "success": True,
            "filename": filename,
            "original_url": f"/static/uploads/{filename}",
            "dimensions": {"width": width, "height": height},
            "context_analysis": context_analysis,
            "recommended_photographer": matched_photographer
        }

    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Image processing error: {str(e)}")

@app.post("/api/enhance")
async def enhance_image(request: Request, payload: EnhanceRequest):
    """
    Applies the selected master photographer's aesthetic recipe to the image.
    Optionally sends an instant WhatsApp or SMS notification if phone number is provided.
    """
    orig_path = UPLOAD_DIR / payload.filename
    if not orig_path.exists():
        raise HTTPException(status_code=404, detail="Original image not found")

    photographer = get_photographer(payload.photographer_id) if payload.photographer_id else None
    if not photographer:
        raise HTTPException(status_code=400, detail="Invalid photographer selected")

    enhanced_filename = f"enhanced_{payload.photographer_id}_{payload.filename}"
    enhanced_path = UPLOAD_DIR / enhanced_filename

    try:
        with Image.open(orig_path) as img:
            intensity = payload.intensity if payload.intensity is not None else 0.85
            enhanced_img, report = enhance_photo(img, photographer, intensity=intensity)
            enhanced_img.save(enhanced_path, quality=95, optimize=True)

        # Construct URLs
        base = str(request.base_url).rstrip("/")
        enhanced_url = f"/static/uploads/{enhanced_filename}"
        full_download_url = f"{base}{enhanced_url}"

        # If phone notification was requested
        notification_result = None
        if payload.phone_number:
            notification_result = send_notification(
                phone_number=payload.phone_number,
                channel=payload.notification_channel or "whatsapp",
                photographer_name=photographer["name"],
                category=photographer["category"],
                download_url=full_download_url
            )

        return {
            "success": True,
            "enhanced_filename": enhanced_filename,
            "enhanced_url": enhanced_url,
            "download_url": full_download_url,
            "photographer": photographer,
            "enhancement_report": report,
            "notification": notification_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement error: {str(e)}")

@app.post("/api/notify")
async def trigger_notification(payload: NotificationRequest):
    """
    Sends or resends a WhatsApp or SMS notification for an existing photo.
    """
    result = send_notification(
        phone_number=payload.phone_number,
        channel=payload.channel,
        photographer_name=payload.photographer_name,
        category=payload.category,
        download_url=payload.download_url
    )
    return result

@app.get("/api/photographers")
async def list_photographers():
    """
    Returns the complete directory of acclaimed master photographers.
    """
    return {"photographers": get_all_photographers()}

@app.get("/api/notifications/logs")
async def notification_logs():
    """
    Returns recent notification attempts.
    """
    return {"logs": get_notification_logs()}

@app.post("/api/settings")
async def update_settings(payload: SettingsUpdateRequest):
    """
    Update Twilio credentials dynamically in memory.
    """
    if payload.twilio_account_sid is not None:
        settings.twilio_account_sid = payload.twilio_account_sid
        os.environ["TWILIO_ACCOUNT_SID"] = payload.twilio_account_sid
    if payload.twilio_auth_token is not None:
        settings.twilio_auth_token = payload.twilio_auth_token
        os.environ["TWILIO_AUTH_TOKEN"] = payload.twilio_auth_token
    if payload.twilio_phone_number is not None:
        settings.twilio_phone_number = payload.twilio_phone_number
        os.environ["TWILIO_PHONE_NUMBER"] = payload.twilio_phone_number
    if payload.twilio_whatsapp_number is not None:
        settings.twilio_whatsapp_number = payload.twilio_whatsapp_number
        os.environ["TWILIO_WHATSAPP_NUMBER"] = payload.twilio_whatsapp_number

    return {"success": True, "message": "Settings updated successfully"}
