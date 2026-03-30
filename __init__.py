from .gemma_api_conditioning_MPS import GemmaMPSAugmentation
# Only the nodes we've actually optimized for Apple Silicon
NODE_CLASS_MAPPINGS = {
    "GemmaMPSAugmentation": GemmaMPSAugmentation
}

# Clean, recognizable display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "GemmaMPSAugmentation": "Gemma API Encode [MPS]"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']