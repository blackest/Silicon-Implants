TLDR:
git clone https://github.com/Blackest/Silicon-Implants comfyui-silicon-implants

Silicon-Implants: MPS-native augmentation nodes for ComfyUI. It's Not PC :)
Tired of sagging? Not getting the performance you expect?
Introducing Silicon-Implants for ComfyUI.

Many nodes are PC-first; if you haven't got CUDA, they fall back to the CPU.
On Apple Silicon, we have Unified Memory and Metal Performance Shaders (MPS).
We aren't built the same. If you want the freedom of not being PC in 2026,
these nodes are for you.

The Strategy: Surgical Augmentation
Silicon-Implants is not a "catch-all" node pack. It is a lean repository of
high-performance alternatives designed to "augment" your setup, not replace it.
PC-centric nodes shuffle GBs of data over the PCI Bus. On Apple Silicon, it's
all the same memory—it’s not a swap, it's deciding who does the job.

Targeted: Only alternatives for bottleneck nodes (Loaders, Encoders,
Samplers) currently crippled by CPU fallback.

Efficiency-First: If it isn't slow, we don't touch it.

Plug & Play: Keep your favorite "pig" repos; just swap in these [MPS]
native versions where it counts.

The Nodes

CLIPLoader (GGUF) [MPS] -- CLIPLoaderGGUFMPS
Wraps city96/ComfyUI-GGUF's CLIPLoaderGGUF and pins load_device,
offload_device, and initial_device to MPS instead of letting them fall
back to CPU. On Apple Silicon, text_encoder_device() and
text_encoder_offload_device() only return the GPU device for
HIGH_VRAM/NORMAL_VRAM (or --gpu-only) -- but cpu_state == CPUState.MPS
always forces vram_state = VRAMState.SHARED, so stock CLIP loaders
quietly run the whole text encoder forward pass on CPU. This one
doesn't. Cut a Krea2 GGUF text encode from ~5 minutes to under a minute
on an M-series Mac.

Loads both formats: .gguf checkpoints go through gguf_clip_loader,
everything else (regular .safetensors) goes through
comfy.utils.load_torch_file -- same as the stock loader. Scaled-FP8
safetensors aren't supported (raises NotImplementedError instead of
silently doing the wrong thing), same limitation as upstream
ComfyUI-GGUF. Requires ComfyUI-GGUF to be installed and enabled; this
node wraps it, it doesn't replace it. Effectively a drop-in swap for
CLIPLoader / DualCLIPLoader / CLIPLoaderGGUF wherever you're loading a
text encoder for image/video generation on Apple Silicon.

Gemma API Encode [MPS] -- GemmaMPSAugmentation
Talks to the LTX-2 API for prompt-embedding conditioning and remaps
the returned CUDA storage tensors so they unpickle correctly on Mac.

Image + String Bridge -- LTX2PassThrough
General-purpose pass-through: takes an image and a string (e.g. a
filename or label) and hands them back unchanged. Useful for keeping
the two traveling together through a graph, or as a stable junction
point. Not MPS-specific -- just a small utility that lives here.

Real-World Silicon Tips
Avoid FP8: It’s not Apple-native and usually crashes.

RAM Management: Monitor Activity Monitor. Orange is okay; Red is bad.
If you're hitting 150GB use with 75GB swap, you're killing your internal SSD.

Browser Choice: Use Safari or run ComfyUI remotely to keep Chrome from
eating your Unified RAM.

Open Build: The "50 Nodes" Vision
The Goal: If 50 developers fix just one bottleneck node, we have a world-class,
native Mac ecosystem in a week.

Contributor Rules:

Author Attribution: Every node file includes a mandatory AUTHOR
attribute. If you fix the node, you get the credit.

MPS-Native: Code must check for MPS and default to BF16/Unified
Memory logic. No lazy CPU fallbacks.

Lean: No unnecessary dependencies. Keep the implants surgical.

Licensing
Since this code is often derivative of other code, licensing derives with it.
Gemma_api_conditioning_MPS.py inherits the LTX-2 licensing (see
LICENSE_LTX2 in this repo).

Note: If you actually meet the requirement for commercial licensing (>$10M
revenue), can I be your friend? :)

Stop the fallbacks. Start using your GPU.
