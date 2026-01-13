---
license: cc-by-nc-4.0
---

Bria Fibo using Amazon Bedrock 

This is a modification of Bria's pipeline block that converts a prompt to a JSON object using Bedrock. See use_fibo.py for usage details.

## Usage

```python
# Create a prompt to generate an initial image
# You can also enable verbose logging per-call by adding verbose=True
output = vlm_pipe(
    prompt="A hyper-detailed, ultra-fluffy owl sitting in the trees at night, looking directly at the camera with wide, adorable, expressive eyes. Its feathers are soft and voluminous, catching the cool moonlight with subtle silver highlights. The owl's gaze is curious and full of charm, giving it a whimsical, storybook-like personality.",
    # verbose=True
)
json_prompt_generate = output.values["json_prompt"]

...

results_generate = pipe(
    prompt=json_prompt_generate, num_inference_steps=50, guidance_scale=5, negative_prompt=negative_prompt
)
```


## Inputs

- `prompt`: A string prompt to convert to a JSON object.

## Outputs

- `json_prompt`: A JSON object representing the prompt.