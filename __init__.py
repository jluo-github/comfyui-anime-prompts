"""
ComfyUI Custom Node: Anime Prompt Loader

Loads prompts from TXT files and adds aesthetic suffixes for
high-fidelity anime image generation.

Author: JL
License: MIT
"""

from .nodes import (
    AnimePromptBatch,
    AnimePromptCombiner,
    AnimePromptLoader,
    AnimePromptRedNote,
    SuffixEditor,
)

__version__ = "1.0.0"

# Node mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "AnimePromptLoader": AnimePromptLoader,
    "AnimePromptBatch": AnimePromptBatch,
    "AnimePromptCombiner": AnimePromptCombiner,
    "AnimePromptRedNote": AnimePromptRedNote,
    "SuffixEditor": SuffixEditor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AnimePromptLoader": "🎨 Anime Prompt Loader",
    "AnimePromptBatch": "🎨 Anime Prompt Batch",
    "AnimePromptCombiner": "🎨 Anime Prompt Combiner",
    "AnimePromptRedNote": "🩷 RedNote Style",
    "SuffixEditor": "✨ Suffix Editor",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "__version__",
]
