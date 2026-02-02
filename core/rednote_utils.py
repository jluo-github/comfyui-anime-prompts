"""
RedNote (XiaoHongShu) Aesthetic Utilities - ARCHITECT FIXED VERSION.
Purged of color bans and lighting conflicts.
"""

from pathlib import Path
from typing import Final

# --- 1. CLEAN NEGATIVE PROMPT (No Color Bans) ---
REDNOTE_NEGATIVE_SUFFIX: Final[str] = (
    "worst quality, low quality, normal quality, lowres, jpeg artifacts, "
    "blurry, signature, watermark, username, text, error, "
    "cropped, out of frame, worst face, mutated face, glitch, "
    "bad anatomy, bad hands, missing fingers, extra digit, fewer digits, "
    "bad proportions, extra limbs, fused fingers, too many fingers, "
    "(large breasts:1.5), (huge breasts:1.5), (cleavage:1.4), nsfw, nude, "
    "(mascara:1.5), (bandaid:1.5), (bandage:1.5), (messy makeup:1.3), "
    "3d, realistic, photo, real life, muscular, simple background, "
    "monochrome, greyscale, (overexposed:1.2), (bright lights:1.2)"
)

# --- 2. POSITIVE SUFFIX (Optimized) ---
REDNOTE_POSITIVE_SUFFIX: Final[str] = (
    ", (perfect cute face:1.4), (beautiful detailed eyes:1.3), "
    "(flat chest:1.2), (petite:1.1), soft focus, messy hair, "
    "masterpiece, best quality, very aesthetic, absurdres, 8k, ultra-detailed, "
    "rednote style"
)

# --- 3. CLEAN PALETTE (No Decimal Noise) ---
STYLES_DICT: Final[dict[str, dict[str, str]]] = {
    "Pastel Dream": {
        "bg": "pastel pink clouds, creamy white, soft diffused lighting, airy",
        "clothes": "casual grey outfit, denim shorts, neutral colors",
    },
    "Midnight Neon": {
        "bg": "dark purple, neon pink highlights, bioluminescence, black background, cinematic lighting",
        "clothes": "white dress, glowing accessories, pristine white fabric",
    },
    "Morning Haze": {
        "bg": "pale blue, white, sunrays, lens flare, ethereal",
        "clothes": "black school uniform, dark navy fabric, sharp contrast",
    },
    "Royal Grief": {
        "bg": "deep violet, gold trim, velvet texture, dramatic shadows, volumetric lighting",
        "clothes": "white gold robe, pristine white, holy vestments",
    },
    "Clinical White": {
        "bg": "pure white, cold lighting, laboratory atmosphere, sterile",
        "clothes": "black coat, dark fashion, black leather",
    },
    "Sunset Melancholy": {
        "bg": "warm orange, deep shadows, silhouette, rim lighting, dusk",
        "clothes": "cyan blue dress, cool techwear, light blue accents",
    },
}


def get_random_palette() -> dict[str, str]:
    """Get random palette without noisy weights."""
    import random

    theme_name = random.choice(list(STYLES_DICT.keys()))
    return STYLES_DICT[theme_name]


# --- 4. MOOD PROMPTS (Unchanged) ---
def get_mood_prompt(level: float) -> str:
    if level < 0.2:
        return "(slight smile:1.2), (gentle expression:1.1), (obedient:1.1), demure"
    elif level < 0.4:
        return "(expressionless:1.3), (neutral face:1.2), (serious:1.2), (looking down:1.1)"
    elif level < 0.6:
        return (
            "(empty eyes:1.5), (hollow gaze:1.4), (dead eyes:1.3), (dissociation:1.3)"
        )
    elif level < 0.8:
        return "(annoyed expression:1.3), (glaring:1.2), (displeased:1.2)"
    else:
        return "(stubborn:1.5), (pouting:1.4), (grumpy:1.4), (angry:1.2), (looking away:1.2)"


# --- 5. COMPATIBILITY STUBS ---
AESTHETIC_KEYWORDS = ["pink", "purple", "white", "sad", "broken"]
EXCLUDE_KEYWORDS = ["harry potter", "monster", "weapon"]


def filter_characters(*args, **kwargs):
    return []


if __name__ == "__main__":
    pass
