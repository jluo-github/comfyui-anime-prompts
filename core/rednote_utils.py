"""
RedNote (XiaoHongShu) Aesthetic Utilities.

Provides filtering, style locking, and mood adjustment functions for
the "Pretty/Broken/Pink-Purple-White" aesthetic.
"""

from pathlib import Path
from typing import Final

# --- REDNOTE AESTHETIC CONSTANTS ---

# Keywords to KEEP (Aesthetic Focus)
AESTHETIC_KEYWORDS: Final[list[str]] = [
    "pink",
    "purple",
    "white",
    "sad",
    "crying",
    "broken",
    "grumpy",
    "stubborn",
    "pretty",
    "cute",
]

# Keywords to EXCLUDE (Noise)
EXCLUDE_KEYWORDS: Final[list[str]] = [
    "harry potter",
    "witch",
    "monster",
    "robot",
    "magical",
    "wand",
    "wizard",
    "green",
    "beast",
    "weapon",
    "armor",
    "bandaid",
    "bandage",
    "mascara",
    "goth",
]

# --- STYLE SYSTEM LOCK ---

REDNOTE_POSITIVE_SUFFIX: Final[str] = (
    ", (perfect cute face:1.4), (beautiful detailed eyes:1.3), "
    "(flat chest:1.2), (petite:1.1), soft focus, messy hair, "
    "masterpiece, best quality, very aesthetic, absurdres, newest, sensitive, "
    "highres, complex background, best anatomy, 8k, ultra-detailed, "
    "rednote style"
)

REDNOTE_NEGATIVE_SUFFIX: Final[str] = (
    # Quality blocks
    "worst quality, low quality, normal quality, lowres, jpeg artifacts, "
    "blurry, signature, watermark, username, text, error, "
    "cropped, out of frame, worst face, mutated face, glitch, "
    # Anatomy blocks
    "bad anatomy, bad hands, missing fingers, extra digit, fewer digits, "
    "bad proportions, extra limbs, fused fingers, too many fingers, "
    "long neck, mutated hands, poorly drawn hands, poorly drawn face, "
    "bad feet, missing feet, extra feet, fused bodies, clone, duplicate, "
    # Body type blocks (SFW + Petite)
    "(large breasts:1.5), (huge breasts:1.5), (big breasts:1.4), (medium breasts:1.3), "
    "(cleavage:1.4), (revealing:1.3), nsfw, nude, naked, bare chest, underwear, "
    # Color blocks (keep pink-purple-white only)
    "(green:1.3), (blue dress:1.3), (teal:1.3), (yellow:1.2), (orange:1.2), "
    "(red dress:1.2), (black dress:1.2), (dark colors:1.2), "
    # Aesthetic blocks (RedNote specific)
    "(mascara:1.5), (bandaid:1.5), (bandage:1.5), (black streaks:1.4), "
    "(messy makeup:1.3), (dirty:1.2), (ugly:1.3), (deformed:1.2), "
    # Style blocks
    "3d, realistic, photo, real life, muscle, muscular, "
    "simple background, harsh lighting, monochrome, greyscale, "
    "(overexposed:1.2), (bright lights:1.2), (harsh lighting:1.2), (glowing skin:1.2), "
    "rim lighting, strong backlight, god rays, bloom, volumetric lighting, whiteout, lens flare"
)


def filter_characters(
    input_path: str | Path,
    output_path: str | Path | None = None,
    keep_keywords: list[str] | None = None,
    exclude_keywords: list[str] | None = None,
) -> list[str]:
    """
    Filter character prompts based on aesthetic keywords.

    Logic: Keep lines containing ANY keep_keyword AND containing NO exclude_keyword.

    Args:
        input_path: Path to the source character file.
        output_path: Optional path to save filtered results.
        keep_keywords: Keywords to keep (defaults to AESTHETIC_KEYWORDS).
        exclude_keywords: Keywords to exclude (defaults to EXCLUDE_KEYWORDS).

    Returns:
        List of filtered character lines.
    """
    if keep_keywords is None:
        keep_keywords = AESTHETIC_KEYWORDS
    if exclude_keywords is None:
        exclude_keywords = EXCLUDE_KEYWORDS

    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Character file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    filtered: list[str] = []
    for line in lines:
        tags_lower = line.lower()

        # Check: has ANY keep keyword AND has NO exclude keyword
        has_keep = any(kw in tags_lower for kw in keep_keywords)
        has_exclude = any(kw in tags_lower for kw in exclude_keywords)

        if has_keep and not has_exclude:
            filtered.append(line)

    # Save to output file if specified
    if output_path is not None:
        output_path = Path(output_path)
        with output_path.open("w", encoding="utf-8") as f:
            f.writelines(filtered)

    return filtered


# --- COLOR PALETTE SYSTEM (Chaos Palette) ---

STYLES_DICT: Final[dict[str, dict[str, str]]] = {
    "Pastel Dream": {
        "bg": "pastel pink clouds, creamy white, soft diffused lighting, low saturation, airy",
        "clothes": "casual grey outfit, denim shorts, neutral colors",
    },
    "Midnight Neon": {
        "bg": "dark purple, neon pink highlights, bioluminescence, black background, cinematic lighting",
        "clothes": "white dress, glowing accessories, pristine white fabric",
    },
    "Morning Haze": {
        "bg": "pale blue, white, sunrays, lens flare, light particles, ethereal",
        "clothes": "black school uniform, dark navy fabric, sharp contrast",
    },
    "Royal Grief": {
        "bg": "deep violet, gold trim, velvet texture, dramatic shadows, volumetric lighting",
        "clothes": "white gold robe, pristine white, holy vestments",
    },
    "Clinical White": {
        "bg": "pure white, cold lighting, laboratory atmosphere, sterile, bright",
        "clothes": "black coat, dark fashion, black leather",
    },
    "Sunset Melancholy": {
        "bg": "warm orange, deep shadows, silhouette, rim lighting, dusk",
        "clothes": "cyan blue dress, cool techwear, light blue accents",
    },
}


def get_weighted_color_tag(tag: str) -> str:
    """Apply dynamic random weighting to a color tag."""
    import random

    # Format: (tag:weight)
    # Reduced max weight from 1.1 to 0.9 to fix "too bright/dense" issue
    # New range: 0.4 to 0.9 (Very soft to Moderate)
    weight = round(random.uniform(0.4, 0.9), 2)
    return f"({tag}:{weight})"


def get_random_palette() -> dict[str, str]:
    """
    Get a random color/lighting palette from STYLES_DICT.
    Returns: A dict with 'bg' and 'clothes' keys containing weighted tags.
    """
    import random

    theme_name = random.choice(list(STYLES_DICT.keys()))
    theme_data = STYLES_DICT[theme_name]

    # Apply dynamic weights to each tag in the palette
    bg_tags = [
        get_weighted_color_tag(tag.strip()) for tag in theme_data["bg"].split(", ")
    ]
    clothes_tags = [
        get_weighted_color_tag(tag.strip()) for tag in theme_data["clothes"].split(", ")
    ]

    return {
        "bg": ", ".join(bg_tags),
        "clothes": ", ".join(clothes_tags),
    }


def apply_rednote_style(
    positive: str,
    negative: str,
) -> tuple[str, str]:
    """
    Applies the RedNote aesthetic style to positive and negative prompts.
    Appends REDNOTE_POSITIVE_SUFFIX (plus a dynamic random color palette)
    and prepends REDNOTE_NEGATIVE_SUFFIX to negative prompt.

    Args:
        positive: The base positive prompt.
        negative: The base negative prompt.

    Returns:
        Tuple of (styled_positive, styled_negative).
    """
    # Get a random color palette with chaos/dynamic weighting
    palette = get_random_palette()

    # --- CRITICAL LIGHTING FIX ---
    # Strip static lighting tags from input to prevent "whiteout"
    # These must be removed so the Palette can control the light.
    clean_positive = positive
    for tag in ["bloom", "dreamy atmosphere", "soft lighting"]:
        clean_positive = clean_positive.replace(tag, "")

    # Append palette + suffix
    # Structure: [BG], [Prompt], [Clothes], [Suffix]
    styled_positive = (
        f"{palette['bg']}, {clean_positive.rstrip(', ')}, {palette['clothes']}"
        + REDNOTE_POSITIVE_SUFFIX
    )

    styled_negative = REDNOTE_NEGATIVE_SUFFIX + ", " + negative.lstrip(", ")
    return styled_positive, styled_negative


def get_mood_prompt(level: float) -> str:
    """
    Get mood-specific prompt modifiers based on fine-grained emotion level.
    Scale: 0.0 (Polite) -> 0.5 (Empty/Stoned) -> 1.0 (Stubborn).
    """
    if level < 0.2:
        # Stage 1: The Polite Mask (0.0 - 0.19)
        return (
            "(slight smile:1.2), (gentle expression:1.1), "
            "(obedient:1.1), (soft eyes:1.1), demure"
        )

    elif level < 0.4:
        # Stage 2: The Serious Fade (0.2 - 0.39)
        return (
            "(expressionless:1.3), (neutral face:1.2), "
            "(serious:1.2), (closed mouth:1.2), (looking down:1.1)"
        )

    elif level < 0.6:
        # Stage 3: The "Stoned" Anchor (The Void) (0.4 - 0.59)
        return (
            "(empty eyes:1.5), (hollow gaze:1.4), (dead eyes:1.3), "
            "(dazed:1.2), (parted lips:1.1), (dissociation:1.3)"
        )

    elif level < 0.8:
        # Stage 4: The Annoyance (0.6 - 0.79)
        return (
            "(annoyed expression:1.3), (glaring:1.2), "
            "(furrowed brow:1.1), (displeased:1.2), (sharp eyes:1.1)"
        )

    else:
        # Stage 5: The Stubborn Wall (0.8 - 1.0)
        return (
            "(stubborn:1.5), (pouting:1.4), (grumpy:1.4), "
            "(angry:1.2), (looking away:1.2), (cheek puff:1.1)"
        )


# --- CLI SCRIPT ---

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python rednote_utils.py <input_file> [output_file]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "rednote_filtered.txt"

    try:
        filtered = filter_characters(input_file, output_file)
        print(
            f"✅ Filter complete. {len(filtered)} 'Pretty/Broken' characters saved to {output_file}"
        )
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
