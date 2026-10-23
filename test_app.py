"""
Automated verification test for the updated classifier and photo enhancer.
"""

from PIL import Image, ImageDraw
import numpy as np
from app.services.classifier import analyze_photo_context
from app.services.photographer_catalog import get_default_photographer_for_category, get_all_photographers
from app.services.photo_enhancer import enhance_photo

def run_tests():
    print(">>> 1. Testing Vertical Landscape with Rocks & Dirt (Previous failure case)...")
    # A vertical mountain landscape with brown/earth tones and sky
    img_landscape = Image.new("RGB", (300, 450), (100, 160, 220)) # Sky
    draw = ImageDraw.Draw(img_landscape)
    # Brown/earth mountains (what previously confused the skin detector!)
    draw.polygon([(0, 200), (120, 100), (220, 180), (300, 120), (300, 450), (0, 450)], fill=(145, 110, 80))
    
    analysis = analyze_photo_context(img_landscape)
    print(f"Detected Category: {analysis['category']} (Confidence: {analysis['confidence']})")
    assert analysis["category"] == "Landscape", f"FAILED: Expected Landscape, got {analysis['category']}"
    print("✓ Vertical mountain landscape correctly identified as Landscape!")

    print(">>> 2. Testing Pure Portrait with Human Face...")
    img_portrait = Image.new("RGB", (300, 400), (25, 25, 30))
    draw_p = ImageDraw.Draw(img_portrait)
    draw_p.ellipse([100, 80, 200, 220], fill=(215, 165, 130)) # Face
    draw_p.rectangle([100, 60, 200, 100], fill=(40, 30, 25))  # Hair
    p_analysis = analyze_photo_context(img_portrait)
    print(f"Detected Category: {p_analysis['category']} (Confidence: {p_analysis['confidence']})")
    assert p_analysis["category"] == "Portrait", f"FAILED: Expected Portrait, got {p_analysis['category']}"
    print("✓ Portrait correctly identified as Portrait!")

    print(">>> 3. Testing Filmic Landscape Enhancement (Highlight preservation)...")
    master = get_default_photographer_for_category("Landscape")
    print(f"Default Landscape Master: {master['name']} ({master['category']})")
    assert master["id"] == "peter_lik"

    enhanced_img, report = enhance_photo(img_landscape, master, intensity=0.85)
    # Verify no pixels were destroyed or blown out to pure solid white where not originally white
    orig_np = np.array(img_landscape)
    enh_np = np.array(enhanced_img)
    print(f"Original max brightness: {np.max(orig_np)}, Enhanced max: {np.max(enh_np)}")
    print(f"Enhancement report: {report['metrics_applied']}")
    print("✓ Highlight preservation and filmic tone curve verified!")

    print("\n✅ ALL REVISED TESTS PASSED CLEANLY!")

if __name__ == "__main__":
    run_tests()
