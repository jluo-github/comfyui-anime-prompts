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
    NEGATIVE_PRESETS,
    PRESETS,
    QUALITY_TAGS,
)
from ..core.file_utils import (
    get_available_txt_files,
    get_prompt_file_path,
    parse_prompt_file,
)
from ..core.rednote_utils import (
    REDNOTE_CHARACTER,
    REDNOTE_NEG_BASE,
    REDNOTE_NEG_SAFETY,
    REDNOTE_NEGATIVE_SUFFIX,
    REDNOTE_POSITIVE_SUFFIX,
    REDNOTE_STYLE,
    get_mood_prompt,
)

ALLOWED_COLORS = [
    "pink",
    "light_pink",
    "white",
    "purple",
    "violet",
    "lilac",
    "lavender",
]


class AnimePromptRedNote:
    CATEGORY = "prompt/anime"
    FUNCTION = "generate_rednote"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt", "negative", "character_name", "mood_tags")
    OUTPUT_IS_LIST = (True, False, True, True)

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        txt_files = get_available_txt_files()
        default_style = (
            "style_names_v1.txt"
            if "style_names_v1.txt" in txt_files
            else (txt_files[0] if txt_files else "")
        )

        # Presets: RedNote (default) + standard presets
        preset_list = ["RedNote"] + list(PRESETS.keys())

        return {
            "required": {
                "prompt_file": (
                    txt_files,
                    {"default": txt_files[0] if txt_files else ""},
                ),
                "style_file": (txt_files, {"default": default_style}),
                "start_index": (
                    "INT",
                    {"default": 0, "min": 0, "max": 99999, "step": 1},
                ),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 1000, "step": 1}),
                "preset": (preset_list, {"default": "RedNote"}),
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
                "enable_style_lock": (
                    "BOOLEAN",
                    {"default": True},
                ),  # Now actually works
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
        self,
        prompt_file,
        style_file,
        start_index,
        batch_size,
        preset,
        mode,
        mood_level,
        enable_style_lock,
        random_action,
        random_background,
        random_camera,
        custom_positive="",
        custom_negative="",
        seed=0,
    ):
        # 1. Load Files
        try:
            char_prompts = parse_prompt_file(get_prompt_file_path(prompt_file))
            style_prompts = parse_prompt_file(get_prompt_file_path(style_file))
        except Exception:
            return (["Error loading files"], "", ["Error"], ["Error"])

        if not char_prompts:
            return (["Error: No prompts"], "", ["Error"], ["Error"])

        # 2. Filter Colors
        filtered_prompts = []
        for p in char_prompts:
            if any(c in p.tags.lower() for c in ALLOWED_COLORS):
                filtered_prompts.append(p)
        target_list = filtered_prompts if filtered_prompts else char_prompts

        # Initialize outputs
        prompts_out = []
        character_names_out = []
        mood_tags_out = []

        random.seed(seed)

        total_chars = len(target_list)
        total_styles = len(style_prompts) if style_prompts else 0

        # Resolve Preset Values
        # If "RedNote", we use the RedNote specific style tag.
        # If other, we use PRESETS[preset] (which usually includes QUALITY_TAGS) and skip RedNote style.
        preset_suffix_start = ""
        preset_style_end = ""
        preset_negative_add = ""

        if preset == "RedNote":
            preset_suffix_start = QUALITY_TAGS  # Start with Quality
            preset_style_end = REDNOTE_STYLE  # End with RedNote Aesthetics
            preset_negative_add = ""  # RedNote negative handled separately/combined
        else:
            preset_suffix_start = PRESETS.get(
                preset, ""
            )  # This usually has Quality Tags inside
            preset_style_end = ""  # No RedNote aesthetics
            preset_negative_add = NEGATIVE_PRESETS.get(preset, "")

        # 3. Batch Loop
        for i in range(batch_size):
            # Calculate current index for sequential character access
            current_index = start_index + i

            # Select Character
            if mode == "random":
                char_idx = random.randint(0, total_chars - 1)
            else:
                char_idx = current_index % total_chars
            entry = target_list[char_idx]

            # 4. Select Style (RESTORED LOCK LOGIC)
            style_tag = ""
            if style_prompts:
                if enable_style_lock:
                    style_idx = current_index % total_styles
                else:
                    style_idx = random.randint(0, total_styles - 1)

                style_tag = style_prompts[style_idx].tags.strip().rstrip(",")

            # 5. Assemble Components
            parts = []

            # A. Start Preset (Quality / Base Style)
            if preset_suffix_start:
                parts.append(preset_suffix_start)

            # A.1. RedNote Aesthetic (Reordered: Start)
            if preset_style_end:
                parts.append(preset_style_end.lstrip(", ").strip())

            # C. Random Style File Tag
            if style_tag:
                parts.append(style_tag)

            # D. Character Tags
            parts.append(entry.tags.strip().rstrip(","))

            # E. Mode Dynamics
            if random_action:
                selected_action = random.choice(ACTIONS)
                parts.append(selected_action)
                if (
                    "hugging knees" in selected_action
                    or "sitting" in selected_action
                    or "lying" in selected_action
                ):
                    parts.append("(white lace safety shorts:1.3)")

            if random_background:
                parts.append(random.choice(BACKGROUNDS))
            if random_camera:
                parts.append(random.choice(CAMERA_EFFECTS))

            # F. Mood
            mood_tags = get_mood_prompt(mood_level)
            parts.append(mood_tags)

            # G. End Presets
            # (RedNote Aesthetic moved to start)

            # 2. Character/Safety (ALWAYS applied)
            parts.append(REDNOTE_CHARACTER.lstrip(", ").strip())

            # H. Custom
            if custom_positive.strip():
                parts.append(custom_positive.strip())

            final_prompt = ", ".join(filter(None, parts))

            prompts_out.append(final_prompt)
            character_names_out.append(entry.character_name)
            mood_tags_out.append(mood_tags)

        # 6. Negative
        # Strategy:
        # A. Base Negative (Quality/Structure) -> Depends on Preset
        # B. Safety Negative (NSFW/Safety) -> ALWAYS Applied (Critical for this node)

        negative_parts = []

        # A. Base Negative
        if preset == "RedNote":
            negative_parts.append(REDNOTE_NEG_BASE)
        elif preset_negative_add:
            negative_parts.append(preset_negative_add)
        else:
            # Fallback if other preset has no specific negative, use RedNote Base?
            # Or just nothing? Usually safer to have some quality control.
            # Let's use RedNote Base as fallback if preset_negative_add is empty.
            if not preset_negative_add:
                negative_parts.append(REDNOTE_NEG_BASE)

        # B. Safety Negative (ALWAYS)
        negative_parts.append(REDNOTE_NEG_SAFETY)

        # C. Custom Negative
        if custom_negative.strip():
            negative_parts.append(custom_negative.strip())

        final_negative = ", ".join(filter(None, negative_parts))

        return (prompts_out, final_negative, character_names_out, mood_tags_out)
