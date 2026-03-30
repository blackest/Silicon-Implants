"""
Silicon-Implants: Gemma API Text Encode
AUTHOR: Blackest
STRATEGY: Surgical MPS Augmentation
LICENCE: LICENCED under the LTX2 Licence included in this repository
"""
import torch
import io
import logging
import pickle
import requests
import folder_paths # type: ignore
from safetensors import safe_open

logger = logging.getLogger(__name__)

LTXV_API_BASE_URL = "https://api.ltx.video"
UPDATE_MESSAGE = "Silicon-Implants Note: If error persists, the node might be outdated or the API schema changed."
INVALID_API_KEY_MESSAGE = "Invalid API key. Generate a new one at: https://console.ltx.video/"
MISSING_MODEL_ID_MESSAGE = "Model ID cannot be identified from the provided checkpoint."

def extract_model_id(ckpt_name: str) -> str:
    model_id_key = "encrypted_wandb_properties"
    full_path = folder_paths.get_full_path_or_raise("checkpoints", ckpt_name)
    with safe_open(full_path, framework="pt", device="cpu") as f:
        metadata = f.metadata()
        if not metadata or model_id_key not in metadata:
            raise ValueError(f"Silicon-Implants: {MISSING_MODEL_ID_MESSAGE}")
        return metadata[model_id_key]

class GemmaMPSAugmentation:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": "", "placeholder": "API_KEY"}),
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "enhance_prompt": ("BOOLEAN", {"default": True}),
                "ckpt_name": (folder_paths.get_filename_list("checkpoints"),),
            },
        }

    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("conditioning",)
    FUNCTION = "encode"
    CATEGORY = "Silicon-Implants/API"

    def encode(self, api_key: str, prompt: str, ckpt_name: str, enhance_prompt: bool = False):
        if not api_key: 
            raise ValueError(f"Silicon-Implants: {INVALID_API_KEY_MESSAGE}")
        
        model_id = extract_model_id(ckpt_name)
        payload = {"prompt": prompt, "model_id": model_id, "enhance_prompt": enhance_prompt}
        
        logger.info(f"Silicon-Implants: Requesting MPS-mapped conditioning...")
        
        try:
            response = requests.post(
                f"{LTXV_API_BASE_URL}/v1/prompt-embedding",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                timeout=60,
            )

            # Specific check for Auth errors
            if response.status_code == 401:
                raise RuntimeError(f"Silicon-Implants: {INVALID_API_KEY_MESSAGE}")
            elif response.status_code != 200:
                raise RuntimeError(f"API Error {response.status_code}: {response.text}")

            # --- APPLE SILICON DIRECT PICKLE PATCH ---
            class M2_Unpickler(pickle.Unpickler):
                def find_class(self, module, name):
                    if module == 'torch.storage' and 'CUDA' in name:
                        return getattr(torch, 'FloatStorage')
                    return super().find_class(module, name)

            orig_validate = torch.serialization._validate_device
            torch.serialization._validate_device = lambda loc, back: torch.device('cpu')
            
            try:
                with io.BytesIO(response.content) as data_stream:
                    data = M2_Unpickler(data_stream).load()
                
                def to_mps_ready(obj):
                    if isinstance(obj, torch.Tensor): return obj.detach().to('cpu')
                    if isinstance(obj, dict): return {k: to_mps_ready(v) for k, v in obj.items()}
                    if isinstance(obj, list): return [to_mps_ready(x) for x in obj]
                    return obj

                conditioning = to_mps_ready(data)
                
            finally:
                torch.serialization._validate_device = orig_validate
            # --- END PATCH ---

            return (conditioning,)

        except Exception as e:
            # If we already raised a specific RuntimeError/ValueError, just pass it up
            if "Silicon-Implants" in str(e):
                raise e
            raise RuntimeError(f"Silicon-Implants API Fail: {str(e)}\n{UPDATE_MESSAGE}")