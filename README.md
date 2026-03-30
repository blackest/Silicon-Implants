Silicon-Implants: MPS-native augmentation nodes for ComfyUI. It's Not PC :)

Tired of sagging? not getting the performance you expect?
 
introducing SiliconImplants for ComfyUI.

It is the answer to some of your performance issues on Apple Silicon. 

Stopping the "Windows Mime" on Apple Silicon.

Many Nodes are PC first and foremost if you havent got CUDA then run on CPU.

We don't have cuda but we do have MPS on Apple Silicon with unified memory
clearly we are not built the same. If you want to have the freedom of not 
being PC in 2026 these nodes are for you. 

I can't rewrite every node pack out there and keep up with the nightly update 
schedule, but its not necessary to do so we just need alternatives that are
optimised for mps usage generally PC centric nodes are all about keeping as 
little as possible in VRAM and switching out to RAM whenever possible, 
This involves copying GB's of  data over the PCI Bus back and forth. CUDA is
very  fast but it has to wait for this shuffling around, meanwhile we have 
Apple Silicon and the metal performance shaders. 

Apple Silicon its all the same memory, its not a swop its deciding who does 
the job. so when they say no CUDA ok fall back to CPU because they didnt even 
check for MPS. We are getting stitched up. This AI work is pretty much always
best performed by the GPU.     

Safe Tensors work well the fp16 of bf16 ones do most of the time some times 
we can get NAN errors when the accuracy slips but FP32 works and GGUF is even
better, bit slower on first run but on apple silicon they can maybe stay 
resident if not we can swap to the internal SSD which is also as fast as 
Apple could make it. 

To be fair Comfyui and models are best on an external SSD.
It's easy to have most of a 2TB drive full of models. Avoid fp8 like the plague
its not apple native, and usually crashes. Be realistic you cant really load 
massive models if you havent got the unified ram for it. Worst i have hit
is something like 150GB in use (with 75GB of swop and thats not good for 
that internal SSD ideally you want no swop but 4 or 5 gb is pretty reasonable. 
in activitity monitor getting into the orange for ram is ok but you don't want 
to be in the red much if at all. As comfyui runs as a server you can access it
remotely so maybe monitor or operate it with another system and you don't have chrome eating up your ram, safari is better on ram but if you are 
squeezed, you want to avoid unnecessary overhead.   

The Strategy: Surgical Augmentation

Silicon-Implants is not a "catch-all" node pack: 

It is a lean repository of high-performance alternatives designed to "augment"
your existing setup, not replace it. For example the free Gemma APi key node
is hard coded to return back to a cuda enabled PC it doesn't need to be and 
thats the first node in this pack.  
 
Targeted: Only specific alternatives for bottleneck nodes (Loaders,
Encoders, Samplers) currently crippled by CPU fallback.

Efficiency-First: We don't waste time updating nodes that work
fine in existing packs. If it isn't slow, we don't touch it.

Plug & Play: Keep your favorite "pig" repos; just swap in these
[MPS] native versions where it counts.

Open Build: The "50 Nodes" Vision

I’m building the core architecture and the first few "implants,"
but this is an open hub for the Apple Silicon community.

The Goal: If 50 developers each fix just one bottleneck node, we
have a world-class, native Mac ecosystem in a week.

Contributor Rules:

Author Attribution: Every node file includes a mandatory AUTHOR
attribute. If you write/fix the node, you get the credit.

MPS-Native: Code must check for MPS and default to BF16/Unified
Memory logic. No lazy CPU fallbacks.

Lean: No unnecessary dependencies. Keep the implants surgical.

Installation & Usage
Clone this repo into your custom_nodes folder.

Restart ComfyUI.

Look for the [MPS] suffix in the node menu.

Swap your slow nodes for the Silicon-Implants versions.

Responsibility Firewall
Each node is attributed to its specific author. If a specific node
breaks, please tag the contributor listed in the node's metadata.
I maintain the framework; the authors maintain their optimizations.

Stop the fallbacks. Start using your GPU.

The aim of this project is a one stop node pack for Apple Silicon that
any Apple Silicon user should find useful. The original devs will be 
updating their nodes so you can't just update thier nodepack with a 
modified python file as it will automatically be replaced with the cuda 
centric one.  By developing silicon implants as a seperate node pack 
then it only gets updated by us. Some nodes may still run on CUDA based 
systems but thats not guarenteed as a lot of optimisation for CUDA low VRAM
setups just slow us down.
