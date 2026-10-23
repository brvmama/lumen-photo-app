"""
Curated catalog of acclaimed master photographers across key photographic contexts.
Refined photographic grading recipes: balanced filmic curves, preserved highlights,
and organic color harmonies that elevate images without destroying natural detail.
"""

from typing import Dict, Any, List

MASTER_PHOTOGRAPHERS: Dict[str, Dict[str, Any]] = {
    # ------------------ LANDSCAPE ------------------
    "peter_lik": {
        "id": "peter_lik",
        "name": "Peter Lik",
        "category": "Landscape",
        "title": "Master of Epic Panoramic Color & Luminous Nature",
        "era": "1959 – Present (Australian)",
        "acclaimed_works": [
            "Phantom (Antelope Canyon, 2014)",
            "Tree of Life",
            "Ghost (Antelope Canyon)"
        ],
        "artistic_philosophy": (
            "Celebrated for vibrant, pristine landscape vistas. Features expansive dynamic range, "
            "radiant saturated foliage and sky harmonies, crisp edge-to-edge clarity, and glowing natural light without harsh clipping."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Potala_Palace_in_Lhasa_Tibet.jpg/640px-Potala_Palace_in_Lhasa_Tibet.jpg",
        "recipe": {
            "is_monochrome": False,
            "contrast": 1.18,
            "shadow_lift": 0.22,
            "highlight_retention": 0.94,
            "saturation": 1.15,
            "vibrance": 1.22,
            "color_temp": 4,
            "clarity": 1.20,
            "sharpness": 1.22,
            "grain": 0.03,
            "vignette": 0.08,
            "split_tone": {"shadow": [25, 45, 65], "highlight": [255, 245, 230]},
            "tone_style": "Vivid panoramic color, lifted shadow detail, pristine skies & rich organic foliage"
        }
    },
    "ansel_adams": {
        "id": "ansel_adams",
        "name": "Ansel Adams",
        "category": "Landscape",
        "title": "Master of the Zone System & Pristine Tonal Contrast",
        "era": "1902 – 1984 (American)",
        "acclaimed_works": [
            "The Tetons and the Snake River (1942)",
            "Moonrise, Hernandez, New Mexico (1941)",
            "Monolith, The Face of Half Dome (1927)"
        ],
        "artistic_philosophy": (
            "Adams developed the Zone System, dividing tone into 10 distinct zones from pure black to pure white. "
            "His landscapes feature breathtaking dynamic range, velvety deep blacks with rich shadow texture, "
            "crisp micro-contrast in rock and water, and luminous, unclipped clouds."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Ansel_Adams_-_National_Archives_79-AA-E01_%28cropped%29.jpg/640px-Ansel_Adams_-_National_Archives_79-AA-E01_%28cropped%29.jpg",
        "recipe": {
            "is_monochrome": True,
            "contrast": 1.28,
            "shadow_lift": 0.18,
            "highlight_retention": 0.96,
            "saturation": 0.0,
            "vibrance": 0.0,
            "color_temp": 0,
            "clarity": 1.26,
            "sharpness": 1.25,
            "grain": 0.08,
            "vignette": 0.10,
            "split_tone": None,
            "tone_style": "High-contrast silver gelatin, zone-balanced deep shadows and luminous clouds"
        }
    },
    "galen_rowell": {
        "id": "galen_rowell",
        "name": "Galen Rowell",
        "category": "Landscape",
        "title": "Vibrant Mountain Light & Golden Hour Radiance",
        "era": "1940 – 2002 (American)",
        "acclaimed_works": [
            "Rainbow over the Potala Palace (1981)",
            "Split Rock, Sierra Nevada",
            "Clearing Storm over Fitz Roy"
        ],
        "artistic_philosophy": (
            "Pioneer of dynamic wilderness photography. Known for graduated optical balancing that preserves "
            "dramatic golden sky illumination with rich foreground detail, warm natural tones, and crisp alpine clarity."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Potala_Palace_in_Lhasa_Tibet.jpg/640px-Potala_Palace_in_Lhasa_Tibet.jpg",
        "recipe": {
            "is_monochrome": False,
            "contrast": 1.16,
            "shadow_lift": 0.25,
            "highlight_retention": 0.92,
            "saturation": 1.18,
            "vibrance": 1.25,
            "color_temp": 8,
            "clarity": 1.18,
            "sharpness": 1.20,
            "grain": 0.04,
            "vignette": 0.08,
            "split_tone": {"shadow": [30, 45, 65], "highlight": [255, 240, 215]},
            "tone_style": "Golden hour alpine warmth, balanced graduated sky, saturated natural hues"
        }
    },
    "sebastiao_salgado": {
        "id": "sebastiao_salgado",
        "name": "Sebastião Salgado",
        "category": "Landscape",
        "title": "Epic Earth & Dramatic Atmospheric Tonality",
        "era": "1944 – Present (Brazilian)",
        "acclaimed_works": [
            "Genesis (2013)",
            "Workers (1993)",
            "Kafue National Park, Zambia"
        ],
        "artistic_philosophy": (
            "Monumental and elemental scale. Salgado uses deep, ink-rich shadows, radiant atmospheric backlighting, "
            "dramatic cloud formations, and sublime natural textures."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Sebasti%C3%A3o_Salgado_in_2016.jpg/640px-Sebasti%C3%A3o_Salgado_in_2016.jpg",
        "recipe": {
            "is_monochrome": True,
            "contrast": 1.34,
            "shadow_lift": 0.12,
            "highlight_retention": 0.95,
            "saturation": 0.0,
            "vibrance": 0.0,
            "color_temp": 0,
            "clarity": 1.30,
            "sharpness": 1.28,
            "grain": 0.14,
            "vignette": 0.15,
            "split_tone": {"shadow": [20, 22, 26], "highlight": [250, 246, 240]},
            "tone_style": "Dramatic inky monochrome with velvety midtones and intense cloud micro-detail"
        }
    },

    # ------------------ PORTRAIT ------------------
    "steve_mccurry": {
        "id": "steve_mccurry",
        "name": "Steve McCurry",
        "category": "Portrait",
        "title": "Iconic Kodachrome Colors & Soulful Eyes",
        "era": "1950 – Present (American)",
        "acclaimed_works": [
            "Afghan Girl (Sharbat Gula, 1984)",
            "Fishermen at Weligama, Sri Lanka (1995)",
            "Dust Storm, Rajasthan (1983)"
        ],
        "artistic_philosophy": (
            "Master of human gaze and rich, tactile color harmonies. McCurry employs Kodachrome-inspired "
            "deep primary colors, glowing ochres, and natural warm skin tones while eyes pop with piercing clarity."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Steve_McCurry_2015.jpg/640px-Steve_McCurry_2015.jpg",
        "recipe": {
            "is_monochrome": False,
            "contrast": 1.15,
            "shadow_lift": 0.18,
            "highlight_retention": 0.94,
            "saturation": 1.14,
            "vibrance": 1.18,
            "color_temp": 6,
            "clarity": 1.14,
            "sharpness": 1.22,
            "grain": 0.05,
            "vignette": 0.12,
            "split_tone": {"shadow": [35, 42, 50], "highlight": [255, 242, 225]},
            "tone_style": "Kodachrome warmth, organic skin tones, rich jewel tones with eye clarity"
        }
    },
    "annie_leibovitz": {
        "id": "annie_leibovitz",
        "name": "Annie Leibovitz",
        "category": "Portrait",
        "title": "Painterly Editorial Lighting & Atmospheric Warmth",
        "era": "1949 – Present (American)",
        "acclaimed_works": [
            "John Lennon and Yoko Ono (1980)",
            "Queen Elizabeth II at Buckingham Palace",
            "Vanity Fair Hollywood Portfolios"
        ],
        "artistic_philosophy": (
            "Theatrical lighting inspired by Dutch Old Masters. Features elegant color palettes, "
            "soft feathered rim lighting, cool desaturated background shadows, and glowing sculpted skin."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Annie_Leibovitz_2008.jpg/640px-Annie_Leibovitz_2008.jpg",
        "recipe": {
            "is_monochrome": False,
            "contrast": 1.12,
            "shadow_lift": 0.20,
            "highlight_retention": 0.92,
            "saturation": 1.05,
            "vibrance": 1.10,
            "color_temp": 4,
            "clarity": 1.10,
            "sharpness": 1.16,
            "grain": 0.06,
            "vignette": 0.14,
            "split_tone": {"shadow": [45, 55, 68], "highlight": [250, 242, 230]},
            "tone_style": "Painterly Rembrandt-style contrast, soft feathered highlights, balanced tonal curve"
        }
    },
    "yousuf_karsh": {
        "id": "yousuf_karsh",
        "name": "Yousuf Karsh",
        "category": "Portrait",
        "title": "Monumental Studio Chiaroscuro & Dramatic Character",
        "era": "1908 – 2002 (Armenian-Canadian)",
        "acclaimed_works": [
            "The Roaring Lion (Winston Churchill, 1941)",
            "Albert Einstein (1948)",
            "Ernest Hemingway (1957)"
        ],
        "artistic_philosophy": (
            "Carved rim-lighting that illuminates character and dignity. High-contrast monochrome, sculpted cheekbones, "
            "radiant hands and eyes against pure deep theatrical shadows."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Winston_Churchill_by_Yousuf_Karsh%2C_1941.jpg/640px-Winston_Churchill_by_Yousuf_Karsh%2C_1941.jpg",
        "recipe": {
            "is_monochrome": True,
            "contrast": 1.32,
            "shadow_lift": 0.10,
            "highlight_retention": 0.95,
            "saturation": 0.0,
            "vibrance": 0.0,
            "color_temp": 0,
            "clarity": 1.30,
            "sharpness": 1.32,
            "grain": 0.10,
            "vignette": 0.20,
            "split_tone": None,
            "tone_style": "Sculptural chiaroscuro studio lighting with deep dramatic blacks and sharp specular highlights"
        }
    },

    # ------------------ ARCHITECTURE ------------------
    "julius_shulman": {
        "id": "julius_shulman",
        "name": "Julius Shulman",
        "category": "Architecture",
        "title": "Mid-Century Modernist Geometry & Luminous Clarity",
        "era": "1910 – 2009 (American)",
        "acclaimed_works": [
            "Case Study House #22 (Stahl House, Los Angeles, 1960)",
            "Kaufmann Desert House (Richard Neutra, Palm Springs, 1947)",
            "Frey House II"
        ],
        "artistic_philosophy": (
            "Flawless linear perspective, pristine geometric lines, "
            "harmonious integration of indoor and outdoor space, and balanced ambient sunset light."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Stahl_House_overview.jpg/640px-Stahl_House_overview.jpg",
        "recipe": {
            "is_monochrome": False,
            "contrast": 1.15,
            "shadow_lift": 0.28,
            "highlight_retention": 0.94,
            "saturation": 1.10,
            "vibrance": 1.15,
            "color_temp": 3,
            "clarity": 1.25,
            "sharpness": 1.25,
            "grain": 0.02,
            "vignette": 0.05,
            "split_tone": {"shadow": [40, 52, 65], "highlight": [255, 250, 240]},
            "tone_style": "Pristine architectural clarity, expanded dynamic range, crisp straight lines"
        }
    },
    "fan_ho": {
        "id": "fan_ho",
        "name": "Fan Ho",
        "category": "Architecture",
        "title": "Geometric Shadows, Atmospheric Fog & Architectural Silhouettes",
        "era": "1931 – 2016 (Hong Kong)",
        "acclaimed_works": [
            "Approaching Shadow (1954)",
            "Lines and Forms (1959)",
            "Sun Rays (1956)"
        ],
        "artistic_philosophy": (
            "Master of dramatic architectural shafts of light cutting through misty alleys, "
            "bold diagonal geometric shadows, and human scale framed within monumental edifices."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Fan_Ho_Approaching_Shadow_style.jpg/640px-Fan_Ho_Approaching_Shadow_style.jpg",
        "recipe": {
            "is_monochrome": True,
            "contrast": 1.35,
            "shadow_lift": 0.06,
            "highlight_retention": 0.95,
            "saturation": 0.0,
            "vibrance": 0.0,
            "color_temp": 0,
            "clarity": 1.35,
            "sharpness": 1.25,
            "grain": 0.12,
            "vignette": 0.18,
            "split_tone": {"shadow": [20, 20, 24], "highlight": [250, 246, 238]},
            "tone_style": "Dramatic geometric chiaroscuro, piercing light beams, high atmospheric contrast"
        }
    },

    # ------------------ STREET & DOCUMENTARY ------------------
    "henri_cartier_bresson": {
        "id": "henri_cartier_bresson",
        "name": "Henri Cartier-Bresson",
        "category": "Street",
        "title": "The Decisive Moment & Timeless 35mm Silver Halide",
        "era": "1908 – 2004 (French)",
        "acclaimed_works": [
            "Behind the Gare Saint-Lazare (1932)",
            "Hyères, France (Bicycle on Spiral Stair, 1932)",
            "Srinagar, Kashmir (1948)"
        ],
        "artistic_philosophy": (
            "Capturing the exact split second where form, emotion, and geometric rhythm converge. "
            "Organic silver-halide film tonality with authentic street presence."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Henri_Cartier-Bresson_1932_style_homage.jpg/640px-Henri_Cartier-Bresson_1932_style_homage.jpg",
        "recipe": {
            "is_monochrome": True,
            "contrast": 1.22,
            "shadow_lift": 0.14,
            "highlight_retention": 0.95,
            "saturation": 0.0,
            "vibrance": 0.0,
            "color_temp": 0,
            "clarity": 1.18,
            "sharpness": 1.20,
            "grain": 0.15,
            "vignette": 0.08,
            "split_tone": None,
            "tone_style": "Authentic Leica 50mm Tri-X film grain, balanced midtones, candid dynamic range"
        }
    },
    "saul_leiter": {
        "id": "saul_leiter",
        "name": "Saul Leiter",
        "category": "Street",
        "title": "Poetic Color Street, Rainy Reflections & Condensed Telephoto Depth",
        "era": "1923 – 2013 (American)",
        "acclaimed_works": [
            "Canopy (1958)",
            "Snow (1960)",
            "Red Cab (1957)"
        ],
        "artistic_philosophy": (
            "Shooting through steamed windows, rain droplets, and mirrors with painterly abstraction, "
            "muted vintage pastel hues, and glowing saturated red accents."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Saul_Leiter_style_street_homage.jpg/640px-Saul_Leiter_style_street_homage.jpg",
        "recipe": {
            "is_monochrome": False,
            "contrast": 1.12,
            "shadow_lift": 0.22,
            "highlight_retention": 0.90,
            "saturation": 1.12,
            "vibrance": 1.16,
            "color_temp": 6,
            "clarity": 1.05,
            "sharpness": 1.12,
            "grain": 0.12,
            "vignette": 0.14,
            "split_tone": {"shadow": [50, 54, 65], "highlight": [248, 225, 205]},
            "tone_style": "Dreamy vintage Kodachrome pastel wash, painterly soft focus, rich warm shadow tones"
        }
    },

    # ------------------ NIGHT & LOW-LIGHT ------------------
    "brassai": {
        "id": "brassai",
        "name": "Brassaï (Gyula Halász)",
        "category": "Night",
        "title": "Paris by Night, Luminous Cobblestones & Deep Mystique",
        "era": "1899 – 1984 (Hungarian-French)",
        "acclaimed_works": [
            "Paris de Nuit (1932)",
            "Lovers in a Small Café (1932)",
            "Pont Neuf in the Mist"
        ],
        "artistic_philosophy": (
            "Long exposure in fog, glistening rain on cobblestones, "
            "silhouetted street lamps casting radiant halos, and velvety deep shadows."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Brassai_style_nocturne.jpg/640px-Brassai_style_nocturne.jpg",
        "recipe": {
            "is_monochrome": True,
            "contrast": 1.32,
            "shadow_lift": 0.08,
            "highlight_retention": 0.96,
            "saturation": 0.0,
            "vibrance": 0.0,
            "color_temp": 0,
            "clarity": 1.25,
            "sharpness": 1.22,
            "grain": 0.16,
            "vignette": 0.20,
            "split_tone": {"shadow": [18, 20, 25], "highlight": [248, 240, 222]},
            "tone_style": "Deep nocturnal blacks, glowing streetlight halos, rich atmospheric film texture"
        }
    },

    # ------------------ MACRO & STILL LIFE ------------------
    "edward_weston": {
        "id": "edward_weston",
        "name": "Edward Weston",
        "category": "Macro",
        "title": "Sculptural Form, Organic Textures & Pure Luminous Tones",
        "era": "1886 – 1958 (American)",
        "acclaimed_works": [
            "Pepper No. 30 (1930)",
            "Nautilus (1927)",
            "Cabbage Leaf (1931)"
        ],
        "artistic_philosophy": (
            "Extraordinary edge-to-edge sharpness, deep glossy tonal graduation, and sculptural textural presence."
        ),
        "reference_image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Weston_Pepper_No_30_study.jpg/640px-Weston_Pepper_No_30_study.jpg",
        "recipe": {
            "is_monochrome": True,
            "contrast": 1.26,
            "shadow_lift": 0.15,
            "highlight_retention": 0.96,
            "saturation": 0.0,
            "vibrance": 0.0,
            "color_temp": 0,
            "clarity": 1.35,
            "sharpness": 1.30,
            "grain": 0.05,
            "vignette": 0.10,
            "split_tone": None,
            "tone_style": "Sculptural Group f/64 razor sharpness, glossy gradations, rich tactile textures"
        }
    }
}

def get_photographers_by_category(category: str) -> List[Dict[str, Any]]:
    cat_lower = category.lower()
    return [p for p in MASTER_PHOTOGRAPHERS.values() if p["category"].lower() == cat_lower]

def get_default_photographer_for_category(category: str) -> Dict[str, Any]:
    cat_map = {
        "landscape": "peter_lik",  # Default to vivid color landscape!
        "portrait": "steve_mccurry",
        "architecture": "julius_shulman",
        "street": "henri_cartier_bresson",
        "night": "brassai",
        "macro": "edward_weston"
    }
    photographer_id = cat_map.get(category.lower(), "peter_lik")
    return MASTER_PHOTOGRAPHERS.get(photographer_id, MASTER_PHOTOGRAPHERS["peter_lik"])

def get_all_photographers() -> List[Dict[str, Any]]:
    return list(MASTER_PHOTOGRAPHERS.values())

def get_photographer(photographer_id: str) -> Dict[str, Any]:
    return MASTER_PHOTOGRAPHERS.get(photographer_id, MASTER_PHOTOGRAPHERS["peter_lik"])
