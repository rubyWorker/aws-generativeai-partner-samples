import json
import os
import sys
import importlib

import torch
from diffusers import BriaFiboPipeline
from diffusers.modular_pipelines import ModularPipeline

# Add the local fibo-bedrock-pipe to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fibo-bedrock-pipe'))

# Force reload of the module to avoid caching issues
if 'bedrock_prompt_to_json' in sys.modules:
    importlib.reload(sys.modules['bedrock_prompt_to_json'])

# Import the local Bedrock-based pipeline
from bedrock_prompt_to_json import BriaFiboBedrockPromptToJson

# -------------------------------
# Load the VLM pipeline (using local Bedrock version)
# -------------------------------
torch.set_grad_enabled(False)

# Create the pipeline using the local Bedrock implementation
# Model IDs are read from environment variables:
# - BASE_MODEL: For text-only operations (default: us.amazon.nova-lite-v1:0)
# - VLM_MODEL: For vision operations (default: us.anthropic.claude-3-5-sonnet-20241022-v2:0)
# NOTE: presumed AWS credentials set in shell to access Bedrock
# Set verbose=True to enable detailed logging of all operations
blocks = BriaFiboBedrockPromptToJson(region_name="us-east-1", verbose=True)

# Initialize the ModularPipeline with the local blocks
vlm_pipe = ModularPipeline(blocks=blocks)

# NOTE: Bedrock VLM uses API calls (no local models, no GPU usage)
# All inference happens on AWS servers via boto3 client


# Load the FIBO pipeline with aggressive memory optimizations
# If you get a 401 error, you need to:
# 1. Get a HuggingFace token from https://huggingface.co/settings/tokens
# 2. Request access to the model at https://huggingface.co/briaai/FIBO
# 3. Either login with: huggingface-cli login
#    Or uncomment the token parameter below and add your token
pipe = BriaFiboPipeline.from_pretrained(
    "briaai/FIBO",
    torch_dtype=torch.bfloat16,
    use_safetensors=True,
    low_cpu_mem_usage=True,  # Reduce CPU memory during loading
    # token="hf_YOUR_TOKEN_HERE",  # Uncomment and add your token if needed
)

# Use sequential CPU offload for T4 GPU (15GB VRAM)
# This keeps only the active component on GPU, rest on CPU
# Slower but fits in memory
pipe.enable_sequential_cpu_offload()

# Additional memory optimizations (only use methods that BriaFiboPipeline supports)
try:
    pipe.enable_attention_slicing(1)  # Most aggressive slicing (slice_size=1)
except AttributeError:
    pass  # Not supported by this pipeline

try:
    pipe.enable_vae_slicing()  # Reduces VAE memory usage
except AttributeError:
    pass  # Not supported by this pipeline

try:
    pipe.enable_vae_tiling()  # Process VAE in tiles for large images
except AttributeError:
    pass  # Not supported by this pipeline

# -------------------------------
# Run Prompt to JSON
# -------------------------------

# Create a prompt to generate an initial image
# You can also enable verbose logging per-call by adding verbose=True
output = vlm_pipe(
    prompt="A hyper-detailed, ultra-fluffy owl sitting in the trees at night, looking directly at the camera with wide, adorable, expressive eyes. Its feathers are soft and voluminous, catching the cool moonlight with subtle silver highlights. The owl's gaze is curious and full of charm, giving it a whimsical, storybook-like personality.",
    # verbose=True  # Uncomment to enable verbose logging for this call only
)
json_prompt_generate = output.values["json_prompt"]

def get_default_negative_prompt(existing_json: dict) -> str:
    negative_prompt = ""
    style_medium = existing_json.get("style_medium", "").lower()
    if style_medium in ["photograph", "photography", "photo"]:
        negative_prompt = """{'style_medium':'digital illustration','artistic_style':'non-realistic'}"""
    return negative_prompt


negative_prompt = get_default_negative_prompt(json.loads(json_prompt_generate))

print("\nSaving JSON prompt to file...")
with open("image_generate_json_prompt.json", "w") as f:
    f.write(json_prompt_generate)
print(f"JSON prompt saved to: image_generate_json_prompt.json")

# -------------------------------
# Run Image Generation
# -------------------------------
# Generate the image from the structured json prompt
print("\nGenerating image from JSON prompt...")
results_generate = pipe(
    prompt=json_prompt_generate, num_inference_steps=10, guidance_scale=5, negative_prompt=negative_prompt
)
results_generate.images[0].save("image_generate.png")
print(f"Image saved to: image_generate.png")
    