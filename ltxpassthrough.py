class LTX2PassThrough:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "text_label": ("STRING", {"default": "Input text here"}),
            },
        }

    # You return the same types you took in
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "text_label")
    FUNCTION = "do_nothing"
    CATEGORY = "Silicon-Implants/Utilities"

    def do_nothing(self, image, text_label):
        # We do absolutely nothing to the data.
        # We just hand it back to ComfyUI's orchestrator.
        return (image, text_label)

NODE_CLASS_MAPPINGS = {
    "LTX2PassThrough": LTX2PassThrough
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LTX2PassThrough": "Image + String Bridge"
}