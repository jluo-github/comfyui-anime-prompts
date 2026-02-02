"""
AnimePromptRedNote node for ComfyUI.

Generates prompts with the RedNote (XiaoHongShu) "Pretty/Broken" aesthetic.
Features mood adjustment, style system lock, and pink-purple-white theme enforcement.
"""

import random
from typing import Any

from ..core.constants import (
    ACTIONS,
    BACKGROUNDS,
    CAMERA_EFFECTS,
)
from ..core.file_utils import (
    get_available_txt_files,
    get_prompt_file_path,
    parse_prompt_file,
)
from ..core.rednote_utils import (
    REDNOTE_NEGATIVE_SUFFIX,
    REDNOTE_POSITIVE_SUFFIX,
    get_mood_prompt,
    get_random_palette,
)


class AnimePromptRedNote:
    """
    Generate prompts with RedNote "Pretty/Broken" aesthetic.

    Features:
    - Mood Level (0.0-1.0): Adjust from "obedient/white" to "stubborn/purple"
    - Style Lock: Automatically apply pink-purple-white theme
    - Clean Output: Blocks mascara, bandaids, messy makeup
    - Decoupled Architecture: Strict prompt assembly order

    Inputs:
        prompt_file: Character TXT file
        index: Prompt index
        mode: sequential or random
        mood_level: Emotion intensity (0.0=white/dreaming, 1.0=purple/broken)
        enable_style_lock: Apply RedNote aesthetic suffix
        random_action/background/camera: Dynamic generation options

    Outputs:
        prompt: Complete positive prompt with style lock
        negative: Complete negative prompt with blocks
        character_name: Character name from file
        mood_tags: The mood-specific tags applied
    """

    CATEGORY = "prompt/anime"
    FUNCTION = "generate_rednote"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt", "negative", "character_name", "mood_tags")

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        """Define input parameters for the node."""
        txt_files = get_available_txt_files()

        return {
            "required": {
                "prompt_file": (
                    txt_files,
                    {"default": txt_files[0] if txt_files else ""},
                ),
                "index": (
                    "INT",
                    {"default": 0, "min": 0, "max": 99999, "step": 1},
                ),
                "mode": (["sequential", "random"], {"default": "sequential"}),
                "mood_level": (
                    "FLOAT",
                    {
                        "default": 0.5,
                        "min": 0.0,
                        "max": 1.0,
                        "step": 0.1,
                        "display": "slider",
                    },
                ),
                "enable_style_lock": ("BOOLEAN", {"default": True}),
                "random_action": ("BOOLEAN", {"default": True}),
                "random_background": ("BOOLEAN", {"default": True}),
                "random_camera": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "custom_positive": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "placeholder": "Additional positive tags",
                    },
                ),
                "custom_negative": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": True,
                        "placeholder": "Additional negative tags",
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "display": "number",
                    },
                ),
            },
        }

    def generate_rednote(
        self,
        prompt_file: str,
        index: int,
        mode: str,
        mood_level: float,
        enable_style_lock: bool,
        random_action: bool,
        random_background: bool,
        random_camera: bool,
        custom_positive: str = "",
        custom_negative: str = "",
        seed: int = 0,
    ) -> tuple[str, str, str, str]:
        """
        Generate a prompt with RedNote aesthetic.

        Returns:
            Tuple of (prompt, negative, character_name, mood_tags).
        """
        file_path = get_prompt_file_path(prompt_file)

        try:
            prompts = parse_prompt_file(file_path)
        except (FileNotFoundError, OSError) as e:
            return (f"Error: {e}", "", "", "")

        if not prompts:
            return ("Error: No prompts found", "", "", "")

        total = len(prompts)
        random.seed(seed)

        # Select prompt
        if mode == "random":
            selected_index = random.randint(0, total - 1)
        else:
            selected_index = index % total

        entry = prompts[selected_index]

        # --- 1. PREPARE COMPONENTS ---

        # Mood (Pure Expression)
        mood_tags = get_mood_prompt(mood_level)

        # Palette (Lighting/Color/Clothes)
        palette_bg = ""
        palette_clothes = ""
        if enable_style_lock:
            palette_dict = get_random_palette()
            palette_bg = palette_dict.get("bg", "")
            palette_clothes = palette_dict.get("clothes", "")

        # Character Tags (Cleaned)
        raw_char_tags = entry.tags.strip().rstrip(",")

        # Random Elements
        random_tags = []
        if random_action:
            random_tags.append(random.choice(ACTIONS))
        if random_background:
            random_tags.append(random.choice(BACKGROUNDS))
        if random_camera:
            random_tags.append(random.choice(CAMERA_EFFECTS))

        # Combine Character + Random + Custom
        full_char_list = [raw_char_tags] + random_tags
        if custom_positive.strip():
            full_char_list.append(custom_positive.strip().lstrip(",").strip())

        character_tags = ", ".join(filter(None, full_char_list))

        # --- 2. CLEANING LOGIC ---
        # Strip static lighting tags to prevent "whiteout"
        for tag in ["bloom", "dreamy atmosphere", "soft lighting"]:
            character_tags = character_tags.replace(tag, "")

        # Additional cleanup of double commas
        character_tags = character_tags.replace(", ,", ",").strip(", ")

        # --- 3. FINAL ASSEMBLY ---
        # Order: Masterpiece -> Palette BG -> Character -> Palette Clothes -> Mood -> Suffix

        parts: list[str] = []

        # Prefix
        parts.append("masterpiece, best quality")

        # Palette BG (Atmosphere)
        if palette_bg:
            parts.append(palette_bg)

        # Character (Subject + Action + Scene)
        if character_tags:
            parts.append(character_tags)

        # Palette Clothes (Contrast)
        if palette_clothes:
            parts.append(palette_clothes)

        # Mood (Expression)
        parts.append(mood_tags)

        # Suffix (System)
        if enable_style_lock:
            parts.append(REDNOTE_POSITIVE_SUFFIX.lstrip(", ").strip())

        final_prompt = ", ".join(filter(None, parts))

        # --- NEGATIVE PROMPT ---
        base_negative = custom_negative.strip()
        if enable_style_lock:
            # Add RedNote negative blocks
            final_negative = (
                REDNOTE_NEGATIVE_SUFFIX + ", " + base_negative.lstrip(", ")
            ).strip(", ")
        else:
            final_negative = base_negative

        return (
            final_prompt,
            final_negative,
            entry.character_name,
            mood_tags,
        )
