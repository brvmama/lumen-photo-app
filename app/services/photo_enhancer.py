"""
High-precision photographic enhancement and master style emulation engine.
Features filmic S-curves, preserved highlights, organic vibrance,
sky-protected color grading, and refined micro-clarity without harsh clipping.
"""

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
from typing import Dict, Any, Tuple

def filmic_s_curve(x: np.ndarray, contrast: float) -> np.ndarray:
    """
    Smooth Hermite S-curve that anchors 0.0 and 1.0, gently rolling off highlights
    and deepening blacks without clipping or blowing out clouds/skies.
    """
    if contrast == 1.0:
        return x
    k = max(0.0, contrast - 1.0)
    # Memory-efficient smoothstep
    smooth = (x * x) * (3.0 - 2.0 * x)
    return x * (1.0 - k) + smooth * k

def enhance_photo(
    image: Image.Image,
    photographer: Dict[str, Any],
    intensity: float = 0.85
) -> Tuple[Image.Image, Dict[str, Any]]:
    """
    Applies the photographer's signature enhancement recipe to the image.
    Supports adjustable intensity (0.0 to 1.0) with highlight protection.
    """
    recipe = photographer.get("recipe", {})
    is_monochrome = recipe.get("is_monochrome", False)

    # Scale recipe parameters by user-defined intensity
    contrast_mult = 1.0 + (recipe.get("contrast", 1.15) - 1.0) * intensity
    shadow_lift = recipe.get("shadow_lift", 0.15) * intensity
    highlight_retention = recipe.get("highlight_retention", 0.94)
    saturation_mult = 1.0 + (recipe.get("saturation", 1.12) - 1.0) * intensity
    vibrance_mult = 1.0 + (recipe.get("vibrance", 1.18) - 1.0) * intensity
    color_temp = recipe.get("color_temp", 0) * intensity
    clarity = 1.0 + (recipe.get("clarity", 1.15) - 1.0) * intensity
    sharpness = 1.0 + (recipe.get("sharpness", 1.20) - 1.0) * intensity
    grain_amt = recipe.get("grain", 0.05) * intensity
    vignette_amt = recipe.get("vignette", 0.08) * intensity
    split_tone = recipe.get("split_tone", None)

    # Convert to RGB float32 [0.0, 1.0]
    orig_img = image.convert("RGB")
    max_dim = 1600
    if max(orig_img.size) > max_dim:
        scale = max_dim / max(orig_img.size)
        orig_img = orig_img.resize((int(orig_img.width * scale), int(orig_img.height * scale)), Image.Resampling.LANCZOS)
    arr = np.array(orig_img, dtype=np.float32) / 255.0

    # 1. Shadow Recovery (Gentle power curve on shadows, preserving highlights)
    if shadow_lift > 0:
        shadow_weight = (1.0 - arr) ** 2.0
        arr = arr + shadow_weight * (shadow_lift * 0.25)
        arr = np.clip(arr, 0.0, 1.0)

    # 2. Filmic S-Curve Contrast (Highlight & Shadow protection)
    if contrast_mult != 1.0:
        arr = filmic_s_curve(arr, contrast_mult)
        arr = np.clip(arr, 0.0, 1.0)

    # 3. Highlight Rolloff / Soft Compression
    if highlight_retention < 1.0:
        # Softly roll off upper 25% of luminance without hard threshold
        upper_mask = np.maximum(0.0, arr - 0.75) / 0.25
        arr = arr - (upper_mask ** 1.5) * ((1.0 - highlight_retention) * 0.10)
        arr = np.clip(arr, 0.0, 1.0)

    # 4. Color vs Monochrome Pipeline
    if is_monochrome:
        # Panchromatic Silver Halide spectral response:
        # 34% Red, 54% Green, 12% Blue (creates dramatic clouds and rich foliage)
        lum = 0.34 * arr[:, :, 0] + 0.54 * arr[:, :, 1] + 0.12 * arr[:, :, 2]
        arr[:, :, 0] = lum
        arr[:, :, 1] = lum
        arr[:, :, 2] = lum

        # Optional subtle split-toning (e.g. Salgado / Fan Ho / Brassai)
        if split_tone:
            sh_color = np.array(split_tone.get("shadow", [20, 22, 26]), dtype=np.float32) / 255.0
            hl_color = np.array(split_tone.get("highlight", [250, 246, 240]), dtype=np.float32) / 255.0
            tone_mask = lum[:, :, np.newaxis]
            toned = hl_color * tone_mask + sh_color * (1.0 - tone_mask)
            arr = arr * 0.90 + toned * 0.10  # Very subtle 10% blend
            arr = np.clip(arr, 0.0, 1.0)
    else:
        # Luminance for color grading
        lum = 0.2126 * arr[:, :, 0] + 0.7152 * arr[:, :, 1] + 0.0722 * arr[:, :, 2]
        lum_3d = lum[:, :, np.newaxis]

        # Natural White Balance / Warmth with Sky Protection
        if color_temp != 0:
            # Protect blue skies/water from turning muddy orange:
            # If B > R, reduce warmth impact
            sky_factor = np.clip((arr[:, :, 2] - arr[:, :, 0] + 0.2), 0.0, 1.0)
            warmth_weight = 1.0 - sky_factor * 0.75

            temp_shift = (color_temp / 400.0)
            arr[:, :, 0] = np.clip(arr[:, :, 0] + temp_shift * warmth_weight, 0.0, 1.0)
            arr[:, :, 2] = np.clip(arr[:, :, 2] - (temp_shift * 0.8) * warmth_weight, 0.0, 1.0)

        # Smart Vibrance & Saturation:
        # Vibrance lifts lower saturated tones while leaving already vivid colors untouched
        if saturation_mult != 1.0 or vibrance_mult != 1.0:
            color_max = np.max(arr, axis=2)
            color_min = np.min(arr, axis=2)
            current_saturation = (color_max - color_min) / (color_max + 1e-5)
            # Higher weight for muted areas, lower weight for saturated areas
            vibrance_weight = (1.0 - current_saturation[:, :, np.newaxis]) * (vibrance_mult - 1.0)

            # Apply gentle saturation boost
            effective_mult = np.clip(saturation_mult + vibrance_weight, 0.8, 1.5)
            arr = lum_3d + (arr - lum_3d) * effective_mult
            arr = np.clip(arr, 0.0, 1.0)

        # Subtle Split Toning for Color
        if split_tone:
            sh_color = np.array(split_tone.get("shadow", [30, 45, 65]), dtype=np.float32) / 255.0
            hl_color = np.array(split_tone.get("highlight", [255, 245, 230]), dtype=np.float32) / 255.0
            shadow_factor = np.clip((1.0 - lum_3d * 2.5), 0.0, 1.0) * 0.06
            highlight_factor = np.clip((lum_3d * 2.0 - 1.0), 0.0, 1.0) * 0.05
            arr = arr + shadow_factor * (sh_color - arr) + highlight_factor * (hl_color - arr)
            arr = np.clip(arr, 0.0, 1.0)

    # 5. Film Grain Simulation (subtle, natural)
    if grain_amt > 0:
        h, w, _ = arr.shape
        np.random.seed(42)
        grain = np.random.normal(0, grain_amt * 0.035, (h, w, 1)).astype(np.float32)
        # Visible mostly in midtones
        mid_mask = 1.0 - 2.0 * np.abs(lum_3d if not is_monochrome else arr[:, :, :1] - 0.5)
        arr = arr + grain * np.clip(mid_mask, 0.0, 1.0)
        arr = np.clip(arr, 0.0, 1.0)

    # 6. Natural Lens Vignette
    if vignette_amt > 0:
        h, w, _ = arr.shape
        y_c = np.linspace(-1, 1, h)[:, np.newaxis]
        x_c = np.linspace(-1, 1, w)[np.newaxis, :]
        dist = np.sqrt(x_c ** 2 + y_c ** 2)
        vignette_mask = 1.0 - np.clip((dist - 0.6) / 0.9, 0.0, 1.0) * (vignette_amt * 0.35)
        arr = arr * vignette_mask[:, :, np.newaxis]
        arr = np.clip(arr, 0.0, 1.0)

    # Convert to PIL Image
    enhanced_pil = Image.fromarray((arr * 255.0).astype(np.uint8))

    # 7. Micro-Clarity (High-pass local contrast using memory-safe native C filter)
    if clarity > 1.0:
        percent = int((clarity - 1.0) * 110)
        enhanced_pil = enhanced_pil.filter(ImageFilter.UnsharpMask(radius=4, percent=percent, threshold=2))

    # 8. Razor Sharpness
    if sharpness > 1.0:
        sharpener = ImageEnhance.Sharpness(enhanced_pil)
        enhanced_pil = sharpener.enhance(sharpness)

    enhancement_report = {
        "master_photographer": photographer["name"],
        "category": photographer["category"],
        "is_monochrome": is_monochrome,
        "style_signature": recipe.get("tone_style", "Master photographic grading"),
        "intensity": f"{int(intensity * 100)}%",
        "metrics_applied": {
            "dynamic_range": f"+{int(shadow_lift*100)}% shadow recovery (filmic curve)",
            "contrast_ratio": f"{round(contrast_mult, 2)}x S-Curve",
            "color_grading": "Panchromatic Silver Halide" if is_monochrome else f"Natural Vibrance (+{int((vibrance_mult-1)*100)}%)",
            "highlight_control": "Filmic soft-shoulder rolloff (unclipped)",
            "micro_clarity": f"+{int((clarity-1.0)*100)}% local contrast",
            "sharpness": f"+{int((sharpness-1.0)*100)}% edge definition"
        }
    }

    return enhanced_pil, enhancement_report
