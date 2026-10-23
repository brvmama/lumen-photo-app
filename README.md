# LUMEN | Masterpiece Photo Enhancer

A web application that contextually detects photo scenes (Portrait, Landscape, Architecture, Street, Night, Macro) and enhances them referencing the aesthetic styles and techniques of history's most acclaimed photographers (e.g. Ansel Adams, Steve McCurry, Annie Leibovitz, Julius Shulman, Henri Cartier-Bresson). Features interactive before/after split sliders, high-res download, and instant completion notifications via **WhatsApp** or **SMS**.

---

## ✨ Features

1. **Context-Aware Visual Classification**:
   - Automatically detects whether an uploaded photo is a **Landscape**, **Portrait**, **Architecture**, **Street**, **Night**, or **Macro** scene.
   - Evaluates luminance distribution, skin tone presence, geometric edge density, sky/foliage ratios, and depth falloff.

2. **Acclaimed Master Reference Catalog**:
   - **Landscape**: Ansel Adams (*Zone System, pristine tonal range*), Sebastião Salgado (*epic atmospheric tonality*), Galen Rowell (*vibrant alpine light*).
   - **Portrait**: Steve McCurry (*Kodachrome warmth & striking gaze*), Annie Leibovitz (*painterly Rembrandt lighting*), Yousuf Karsh (*studio chiaroscuro*).
   - **Architecture**: Julius Shulman (*mid-century clarity & clean geometry*), Fan Ho (*architectural shadow silhouettes*).
   - **Street**: Henri Cartier-Bresson (*The Decisive Moment, 35mm silver halide*), Saul Leiter (*poetic color street reflections*).
   - **Night / Low-Light**: Brassaï (*nocturnal fog & cobblestones*).
   - **Macro / Still Life**: Edward Weston (*Group f/64 razor sharpness & sculptural organic forms*).

3. **High-Precision Photographic Enhancement Engine**:
   - Custom 32-bit floating point tone mapping & S-curves.
   - Shadow recovery & highlight compression without banding.
   - Master split-toning & vibrance balancing.
   - Local micro-contrast clarity & unsharp masking.
   - Authentic silver halide / Kodachrome film grain simulation.

4. **Interactive Studio & High-Res Download**:
   - Interactive split before/after comparison slider.
   - Immediate 1-click download of the enhanced high-resolution photo.
   - Full technical breakdown of grading metrics applied.

5. **WhatsApp & SMS Phone Notifications**:
   - Option to enter mobile number for automated WhatsApp or SMS alert when photo enhancement is ready.
   - Native integration with Twilio WhatsApp & SMS API.
   - Zero-setup direct `wa.me` WhatsApp Instant Web Link fallback so anyone can message results to their phone with zero API keys required!

---

## 🚀 Quickstart

### 1. Run the Web Application
```bash
python run.py
```
Open your browser at: **[http://localhost:8000](http://localhost:8000)**

### 2. (Optional) Configure Twilio for WhatsApp / SMS
You can either click **"Notification Settings"** in the top navigation bar of the web app or copy `.env.example` to `.env`:

```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```
*(Note: If Twilio is not configured, the app provides a 1-click "Open in WhatsApp" direct link that works instantly with zero setup).*
