"""
Visual context classification service.
Robust scene classification:
- Distinguishes Landscape, Portrait, Architecture, Street, Night, and Macro
- Accurately discriminates true human faces from natural earth/rocks/sand
- Detects sky/cloud bands, horizons, foliage, and geometric lines
"""

from PIL import Image
import numpy as np
from typing import Dict, Any

def analyze_photo_context(image: Image.Image) -> Dict[str, Any]:
    """
    Analyzes an uploaded PIL Image and returns the detected category, confidence score,
    and visual metadata.
    """
    thumb = image.convert("RGB").resize((128, 128))
    img_np = np.array(thumb, dtype=np.float32)

    width, height = image.size
    aspect_ratio = width / max(height, 1)

    r = img_np[:, :, 0]
    g = img_np[:, :, 1]
    b = img_np[:, :, 2]

    # Luminance (Rec. 709)
    y = 0.299 * r + 0.587 * g + 0.114 * b
    mean_lum = float(np.mean(y))

    # YCbCr Chromaticity
    cb = 128.0 - 0.168736 * r - 0.331264 * g + 0.5 * b
    cr = 128.0 + 0.5 * r - 0.418688 * g - 0.081312 * b

    # Standard Kovac Human Skin Chromaticity Model
    skin_pixels = (cb >= 77) & (cb <= 127) & (cr >= 133) & (cr <= 173) & (y > 40)

    # 1. True Face Oval Concentration vs Background (Crucial to prevent rocks/sand being called a face)
    yy, xx = np.ogrid[:128, :128]
    # Ellipse mask centered in upper-mid where human heads sit
    face_oval = (((yy - 54) ** 2) / (32 ** 2) + ((xx - 64) ** 2) / (24 ** 2)) <= 1.0
    oval_skin_ratio = float(np.mean(skin_pixels[face_oval]))
    outer_skin_ratio = float(np.mean(skin_pixels[~face_oval]))

    # A portrait has high skin concentration inside the oval AND low skin in the outer surroundings
    is_true_face = (oval_skin_ratio > 0.35) and (oval_skin_ratio > (outer_skin_ratio * 1.7 + 0.05))

    # 2. Sky & Horizon Analysis in Upper Third (Landscape signature)
    top_y = y[:45, :]
    dx_top = np.abs(top_y[:, 1:] - top_y[:, :-1])
    dy_top = np.abs(top_y[1:, :] - top_y[:-1, :])
    top_smoothness = float(1.0 / (np.mean(dx_top) + np.mean(dy_top) + 1.0))

    top_r, top_g, top_b = r[:45, :], g[:45, :], b[:45, :]
    # Blue sky
    is_blue_sky = float(np.mean((top_b > top_r + 5) & (top_b > top_g * 0.92))) > 0.18
    # Overcast / white / gray sky (smooth, neutral, bright)
    is_overcast_sky = (float(np.mean(top_y > 130)) > 0.30) and (float(np.mean(np.abs(top_r - top_b))) < 30) and (top_smoothness > 0.10)
    # Golden sunset / sunrise sky
    is_sunset_sky = float(np.mean((top_r > top_b + 20) & (top_r > top_g) & (top_y > 80))) > 0.20 and (top_smoothness > 0.08)

    has_sky = is_blue_sky or is_overcast_sky or is_sunset_sky

    # Foliage and natural terrain
    foliage_ratio = float(np.mean((g > r + 5) & (g > b + 5)))
    water_ratio = float(np.mean((b > r + 15) & (b >= g) & (y < 180)))

    # 3. Night / Low-Light
    dark_ratio = float(np.mean(y < 35))
    bright_specular = float(np.mean(y > 220))
    is_night = ((mean_lum < 65 and dark_ratio > 0.45) or (mean_lum < 45)) and not is_true_face

    # 4. Architecture / Geometric Edges
    dx = np.abs(y[:, 1:] - y[:, :-1])
    dy = np.abs(y[1:, :] - y[:-1, :])
    mean_dx = float(np.mean(dx))
    mean_dy = float(np.mean(dy))
    overall_edge_energy = (mean_dx + mean_dy) / 2.0
    directional_bias = abs(mean_dx - mean_dy) / (mean_dx + mean_dy + 1e-5)

    # 5. Macro (Sharp central subject with blurred perimeter)
    center_y = y[38:90, 38:90]
    center_edge = float(np.mean(np.abs(center_y[:, 1:] - center_y[:, :-1])))
    outer_mask = np.ones((128, 128), dtype=bool)
    outer_mask[38:90, 38:90] = False
    outer_edge = float(np.std(y[outer_mask]))
    macro_ratio = center_edge / (outer_edge + 1.0)

    # Scoring Matrix
    scores = {
        "Landscape": 0.15,
        "Portrait": 0.05,
        "Architecture": 0.10,
        "Street": 0.10,
        "Night": 0.05,
        "Macro": 0.05
    }

    reasons = []

    # Apply Landscape scores
    if has_sky:
        scores["Landscape"] += 0.55
        reasons.append("Identified open sky / horizon atmosphere")
    if foliage_ratio > 0.08:
        scores["Landscape"] += 0.30
        reasons.append(f"Detected natural foliage & vegetation ({round(foliage_ratio*100, 1)}%)")
    if water_ratio > 0.10:
        scores["Landscape"] += 0.25
        reasons.append("Detected water / lake / ocean surface")
    if aspect_ratio >= 1.2 and not is_true_face:
        scores["Landscape"] += 0.15

    # Apply Portrait scores (Strict: requires genuine facial localization)
    if is_true_face:
        scores["Portrait"] += 0.70
        reasons.append("Detected focused human facial structure and skin tones")
    elif oval_skin_ratio > 0.45 and outer_skin_ratio < 0.25:
        scores["Portrait"] += 0.40
        reasons.append("Detected central figure presence")

    # Apply Night scores
    if is_night:
        scores["Night"] += 0.75
        if bright_specular > 0.01:
            scores["Night"] += 0.20
        reasons.append("Detected nocturnal low-key illumination with specular highlights")

    # Apply Architecture scores
    if overall_edge_energy > 8.5 and directional_bias > 0.15 and not has_sky and not is_night:
        scores["Architecture"] += 0.50
        reasons.append("Detected rectilinear structural lines and architectural geometry")
    elif overall_edge_energy > 9.0 and directional_bias > 0.10:
        scores["Architecture"] += 0.30

    # Apply Street scores
    if overall_edge_energy > 8.0 and not has_sky and not is_true_face:
        scores["Street"] += 0.35
        reasons.append("Detected dynamic street/urban textures")

    # Apply Macro scores
    if macro_ratio > 0.55 and not has_sky and not is_true_face and not is_night:
        scores["Macro"] += 0.45
        reasons.append("Detected shallow depth of field with centered subject focus")

    # If it has sky and no face, Landscape strongly dominates
    if has_sky and not is_true_face:
        scores["Landscape"] = max(scores["Landscape"], 0.75)
        scores["Portrait"] = min(scores["Portrait"], 0.15)

    detected_category = max(scores, key=scores.get)
    confidence = min(round(max(0.65, scores[detected_category]), 2), 0.98)

    if not reasons:
        reasons.append(f"Compositional framing indicative of {detected_category}")

    return {
        "category": detected_category,
        "confidence": confidence,
        "aspect_ratio": round(aspect_ratio, 2),
        "mean_luminance": round(mean_lum, 1),
        "reasons": reasons,
        "all_scores": {k: round(v, 2) for k, v in scores.items()}
    }
