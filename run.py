import uvicorn
import os
import sys

# Ensure current directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import socket
    local_ip = "127.0.0.1"
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        pass

    print("=" * 65)
    print("  LUMEN | Masterpiece Photo Enhancer Web App")
    print("  Context-Aware AI Photo Grading & Master Styling")
    print("  WhatsApp & SMS Notifications Enabled")
    print("=" * 65)
    print(f"  Local Desktop:  http://localhost:8000")
    print(f"  Mobile Device:  http://{local_ip}:8000 (same Wi-Fi)")
    print("=" * 65)
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
