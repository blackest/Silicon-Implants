from .gemma_api_conditioning_MPS import GemmaMPSAugmentation
from .ltxpassthrough import LTX2PassThrough
from .clip_loader_gguf_mps import CLIPLoaderGGUFMPS
# Only the nodes we've actually optimized for Apple Silicon
NODE_CLASS_MAPPINGS = {
    "GemmaMPSAugmentation": GemmaMPSAugmentation,
    "LTX2PassThrough": LTX2PassThrough,
    "CLIPLoaderGGUFMPS": CLIPLoaderGGUFMPS,
}

# Clean, recognizable display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GemmaMPSAugmentation": "Gemma API Encode [MPS]",
    "LTX2PassThrough": "Do Nothing Node (Bridge)",
    "CLIPLoaderGGUFMPS": "CLIPLoader (GGUF) [MPS]",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']