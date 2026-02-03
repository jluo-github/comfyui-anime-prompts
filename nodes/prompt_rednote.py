"""
AnimePromptRedNote node for ComfyUI - ARCHITECT STYLE LOCK FIX.
- Style Lock ON: Style follows 'index' (Deterministic/Manual).
- Style Lock OFF: Style is Random (Surprise).
- Kept 'Dynamic Engine' (Combiner quality).
- Kept 'Smart Safety' (Shorts only when sitting).
"""

import random
from typing import Any

from ..core.constants import (
    ACTIONS,
    BACKGROUNDS,
    CAMERA_EFFECTS,
    QUALITY_TAGS,
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
)

ALLOWED_COLORS = ["pink", "white", "purple", "violet", "lilac", "lavender"]
DYNAMIC_TAGS = "dynamic angle, wind, motion blur, dramatic pose, foreshortening"

class AnimePromptRedNote:
    CATEGORY = "prompt/anime"
    FUNCTION = "generate_rednote"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt", "negative", "character_name", "mood_tags")

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        txt_files = get_available_txt_files()
        default_style = "style_names_v1.txt" if "style_names_v1.txt" in txt_files else (txt_files[0] if txt_files else "")

        return {
            "required": {
                "prompt_file": (txt_files, {"default": txt_files[0] if txt_files else ""}),
                "style_file": (txt_files, {"default": default_style}),
                "index": ("INT", {"default": 0, "min": 0, "max": 99999, "step": 1}),
                "mode": (["sequential", "random"], {"default": "sequential"}),
                "mood_level": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1, "display": "slider"}),
                "enable_style_lock": ("BOOLEAN", {"default": True}), # Now actually works
                "random_action": ("BOOLEAN", {"default": True}),
                "random_background": ("BOOLEAN", {"default": True}),
                "random_camera": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "custom_positive": ("STRING", {"default": "", "multiline": True}),
                "custom_negative": ("STRING", {"default": "", "multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
            },
        }

    def generate_rednote(
        self, prompt_file, style_file, index, mode, mood_level, enable_style_lock, 
        random_action, random_background, random_camera, 
        custom_positive="", custom_negative="", seed=0
    ):
        # 1. Load Files
        try:
            char_prompts = parse_prompt_file(get_prompt_file_path(prompt_file))
            style_prompts = parse_prompt_file(get_prompt_file_path(style_file))
        except Exception:
            return ("Error loading files", "", "", "")

        if not char_prompts: return ("Error: No prompts", "", "", "")

        # 2. Filter Colors
        filtered_prompts = []
        for p in char_prompts:
            if any(c in p.tags.lower() for c in ALLOWED_COLORS):
                filtered_prompts.append(p)
        target_list = filtered_prompts if filtered_prompts else char_prompts
        
        # 3. Select Character
        random.seed(seed)
        total_chars = len(target_list)
        
        if mode == "random":
            char_idx = random.randint(0, total_chars - 1)
        else:
            char_idx = index % total_chars
        entry = target_list[char_idx]

        # 4. Select Style (RESTORED LOCK LOGIC)
        style_tag = ""
        if style_prompts:
            total_styles = len(style_prompts)
            if enable_style_lock:
                # Lock ON: Deterministic (Index-based)
                # This ensures if you keep Index the same, Style stays the same.
                style_idx = index % total_styles
            else:
                # Lock OFF: Pure Random
                style_idx = random.randint(0, total_styles - 1)
            
            style_tag = style_prompts[style_idx].tags.strip().rstrip(",")

        # 5. Assemble Components
        parts = []
        parts.append(QUALITY_TAGS)
        parts.append(DYNAMIC_TAGS)
        if style_tag: parts.append(style_tag)
        parts.append(entry.tags.strip().rstrip(","))

        # Dynamics + Smart Safety
        if random_action: 
            selected_action = random.choice(ACTIONS)
            parts.append(selected_action)
            # Smart Safety: Shorts only when sitting
            if "hugging knees" in selected_action or "sitting" in selected_action or "lying" in selected_action:
                parts.append("(white lace safety shorts:1.3)")

        if random_background: parts.append(random.choice(BACKGROUNDS))
        if random_camera: parts.append(random.choice(CAMERA_EFFECTS))

        mood_tags = get_mood_prompt(mood_level)
        parts.append(mood_tags)
        
        # Pure Suffix (Clean)
        parts.append(REDNOTE_POSITIVE_SUFFIX.lstrip(", ").strip())

        if custom_positive.strip(): parts.append(custom_positive.strip())

        final_prompt = ", ".join(filter(None, parts))

        # 6. Negative
        base_negative = custom_negative.strip()
        final_negative = (REDNOTE_NEGATIVE_SUFFIX + ", " + base_negative.lstrip(", ")).strip(", ")

        return (final_prompt, final_negative, entry.character_name, mood_tags)