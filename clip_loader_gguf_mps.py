"""
Silicon-Implants: CLIP Loader (GGUF) [MPS]
AUTHOR: Blackest
STRATEGY: Surgical MPS Augmentation
LICENCE: Apache-2.0 (see LICENSE in this repository)

Wraps city96/ComfyUI-GGUF's CLIPLoaderGGUF. That loader (and comfy.sd.CLIP
underneath it) picks load_device/offload_device/initial_device via
text_encoder_device()/text_encoder_offload_device(), which fall back to CPU
on Apple Silicon because cpu_state == CPUState.MPS forces
vram_state = VRAMState.SHARED, and text_encoder_device() only returns the
GPU device for HIGH_VRAM/NORMAL_VRAM (or --gpu-only). Net effect: GGUF text
encoders run their whole forward pass on CPU. This node pins all three to
MPS instead.
"""
import os
import sys
import logging

import comfy.sd
import comfy.model_management
import folder_paths  # type: ignore

logger = logging.getLogger(__name__)

MISSING_GGUF_PACK_MESSAGE = (
    "Silicon-Implants: requires city96/ComfyUI-GGUF to be installed and enabled "
    "(CLIPLoaderGGUFMPS wraps it, it doesn't replace it)."
)


def _gguf_nodes():
    # ComfyUI keys custom node packages in sys.modules by their absolute
    # install path (nodes.py: sys_module_name = module_path.replace(".", "_x_")),
    # not by the plain folder name, so we match on the path's basename instead.
    for mod_name, mod in list(sys.modules.items()):
        if mod is None or not hasattr(mod, "nodes"):
            continue
        if os.path.basename(mod_name.rstrip("/\\")).lower() == "comfyui-gguf":
            if hasattr(mod.nodes, "CLIPLoaderGGUF"):
                return mod.nodes
    raise RuntimeError(MISSING_GGUF_PACK_MESSAGE)


def _mps_or_stock_device():
    device = comfy.model_management.get_torch_device()
    if comfy.model_management.is_device_mps(device):
        return device
    return comfy.model_management.text_encoder_device()


class CLIPLoaderGGUFMPS:
    @classmethod
    def INPUT_TYPES(cls):
        return _gguf_nodes().CLIPLoaderGGUF.INPUT_TYPES()

    RETURN_TYPES = ("CLIP",)
    FUNCTION = "load_clip"
    CATEGORY = "Silicon-Implants/GGUF"
    TITLE = "CLIPLoader (GGUF) [MPS]"

    def load_clip(self, clip_name, type="stable_diffusion"):
        gguf_nodes = _gguf_nodes()
        clip_path = folder_paths.get_full_path("clip", clip_name)
        clip_type = getattr(comfy.sd.CLIPType, type.upper(), comfy.sd.CLIPType.STABLE_DIFFUSION)
        clip_data = gguf_nodes.CLIPLoaderGGUF().load_data([clip_path])

        device = _mps_or_stock_device()
        logger.info(f"Silicon-Implants: loading GGUF text encoder on {device} (load+offload+initial, no CPU fallback)")

        clip = comfy.sd.load_text_encoder_state_dicts(
            clip_type=clip_type,
            state_dicts=clip_data,
            model_options={
                "custom_operations": gguf_nodes.GGMLOps,
                "load_device": device,
                "offload_device": device,
                "initial_device": device,
            },
            embedding_directory=folder_paths.get_folder_paths("embeddings"),
        )
        clip.patcher = gguf_nodes.GGUFModelPatcher.clone(clip.patcher)

        if clip.patcher.load_device != device:
            logger.warning(
                f"Silicon-Implants: CLIPLoaderGGUFMPS fell back to "
                f"{clip.patcher.load_device} instead of {device} -- this node needs "
                f"an update (upstream comfy.sd.CLIP's device handling likely changed)."
            )

        return (clip,)


NODE_CLASS_MAPPINGS = {
    "CLIPLoaderGGUFMPS": CLIPLoaderGGUFMPS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CLIPLoaderGGUFMPS": "CLIPLoader (GGUF) [MPS]",
}
