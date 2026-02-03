"""Constants and presets for Illustrious-XL anime prompt generation."""

import os
from typing import Final

# Directory containing prompt files
PROMPT_DIR: Final[str] = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# --- 1. CORE QUALITY TAGS ---
QUALITY_TAGS: Final[str] = (
    "masterpiece, best quality, very aesthetic, absurdres, newest, sensitive, "
    "highres, complex background, best anatomy, 8k"
)

# --- 2. NEGATIVE PROMPTS ---
STANDARD_NEGATIVE: Final[str] = (
    "worst quality, low quality, normal quality, lowres, anatomical nonsense, "
    "artistic error, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, "
    "cropped, jpeg artifacts, signature, watermark, username, blurry, artist name, "
    "text, error, 3d, realistic, photo, real life, bad proportions, muscle, muscular"
)

# Default values
DEFAULT_SUFFIX: Final[str] = QUALITY_TAGS
DEFAULT_NEGATIVE: Final[str] = STANDARD_NEGATIVE

# --- 3. STYLE PRESETS (Refined for Girly/Emotional) ---
PRESETS: Final[dict[str, str]] = {
    "none": "",
    "standard": QUALITY_TAGS,
    "dynamic": f"{QUALITY_TAGS}, dynamic angle, wind, motion blur, dramatic pose, foreshortening",
    "atmospheric": f"{QUALITY_TAGS}, cinematic lighting, depth of field, tyndall effect, volumetric lighting, emotional, soft focus",
    "flat": f"{QUALITY_TAGS}, (vibrant colors:1.2), flat color, vector, bold lines, simple background, colorful, white background",
    # Renamed "Fantasy" to "Dreamy" (No magic, just soft vibes)
    "dreamy": f"{QUALITY_TAGS}, pastel colors, soft lighting, bloom, dreamy atmosphere, ethereal, delicate",
    "gothic": f"{QUALITY_TAGS}, dark theme, gothic, high contrast, chiaroscuro, mysterious, shadows",
}

# --- 4. MATCHING NEGATIVES ---
NEGATIVE_PRESETS: Final[dict[str, str]] = {
    "none": "",
    "standard": f"{STANDARD_NEGATIVE}, simple background",
    "dynamic": f"{STANDARD_NEGATIVE}, static, standing still, boring, simple background",
    "atmospheric": f"{STANDARD_NEGATIVE}, flat color, harsh lighting, simple background",
    "flat": f"{STANDARD_NEGATIVE}, 3d, realistic lighting, gradient, photorealistic, shadow, complex background",
    "dreamy": f"{STANDARD_NEGATIVE}, harsh lighting, horror, technology, modern",
    "gothic": f"{STANDARD_NEGATIVE}, bright, pastel, cheerful, sunshine, simple background",
}

# --- 5. DYNAMIC ACTIONS (Girly, Cute, Emotional - Pose/Expression Only) ---
ACTIONS: Final[list[str]] = [
    # --- 🍞 Cute Eating ---
    "eating toast, holding toast, biting, crumbs on cheek, messy hair, happy",
    "eating strawberry crepe, holding food, puffy cheeks, happy expression, cream on nose",
    "drinking bubble tea, holding cup, straw in mouth, looking at viewer, cute",
    "eating ice cream, licking, cone in hand, summer, sweet, happy smile",
    "cooking, stirring, eggs, messy kitchen, confused",
    # --- 💫 Girly Poses ---
    "peace sign, winking, tilting head, playful smile, looking at viewer",
    "holding hair, wind blowing, eyes closed, soft smile, gentle",
    "finger on lips, shy expression, blushing, looking away, embarrassed",
    "stretching arms up, yawning, sleepy eyes, messy hair, morning",
    "twirling, spinning, skirt flowing, happy, joyful expression",
    # --- 💔 Broken / Emotional ---
    "crying, tears streaming, red eyes, wiping tears, sad, looking down",
    "hugging knees, head down, lonely, empty gaze, vulnerable",
    "looking at phone, waiting, lonely, disappointed, dim lighting",
    "lying down, staring blankly, arm over eyes, exhausted, melancholic",
    "in rain, wet hair, wet clothes, looking up at sky, melancholic",
    # --- 🌸 Soft / Dreamy ---
    "reaching for falling petals, wind in hair, gentle",
    "holding flower, smelling, eyes closed, peaceful, delicate",
    "gazing at sunset, profile view, wind, contemplative, serene",
    # --- 🐱 Cozy ---
    "sleeping, head on arms, peaceful, drooling slightly, cute",
    "hugging plushie, burying face, oversized hoodie, cozy, warm",
    "holding cat, nuzzling, soft expression, cuddling pet",
]

# --- 6. MATCHING BACKGROUNDS (No Magic, Real Places) ---
BACKGROUNDS: Final[list[str]] = [
    # --- 🏫 School & Outdoor ---
    "school classroom, wooden desk, blackboard, windows, sunlight, afternoon",
    "school hallway, lockers, polished floor, sunlight rays, anime school",
    "cherry blossom park, pink flower trees, falling petals, park bench, spring path",
    "sunny beach, ocean waves, sky, clouds, summer, horizon",
    "flower garden, blooming flowers, garden fence, nature, soft sunlight",
    # --- 🏠 Home & Bedroom (Messy/Cozy) ---
    "cluttered bedroom, unmade bed, clothes on floor, computer desk, plushies, lived-in feel",
    "cozy bedroom, fairy lights on wall, pastel bedding, night, warm lamp light",
    "modern kitchen, gas stove, refrigerator, kitchen counter, sink, domestic setting",
    "living room, sofa, television, coffee table, sunlight through curtains",
    "bathroom, tiled walls, bathtub, mirror, steam, soft lighting",
    # --- 🏙️ City & Mood ---
    "rainy city street, reflection in puddles, neon lights, night, atmospheric",
    "convenience store front, bright lights, night, glass door, shelves",
    "rooftop at sunset, chain link fence, warm sky, city skyline, wind",
    "train station platform, waiting area, empty seats, evening light, nostalgic",
]

# --- 7. CAMERA EFFECTS (Simple & Aesthetic) ---
CAMERA_EFFECTS: Final[list[str]] = [
    "from above, looking down, depth of field",
    "from below, looking up, dramatic angle",
    "close-up, portrait, bokeh, focus on face",
    "wide shot, full body, distant view",
    "soft lighting, backlight, rim light, warm tones",
    "soft focus, bloom, dreamy, film grain",
    "side view, profile, wind, hair flowing",
    "pov, first person view, intimate, close",
]
