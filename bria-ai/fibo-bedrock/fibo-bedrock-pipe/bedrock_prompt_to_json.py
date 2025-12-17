import base64
import io
import json
import math
import os
from functools import cache
from typing import List, Optional, Tuple

import boto3
import ujson
from boltons.iterutils import remap
from diffusers.modular_pipelines import InputParam, ModularPipelineBlocks, OutputParam, PipelineState
from PIL import Image
from pydantic import BaseModel, Field


class ObjectDescription(BaseModel):
    description: str = Field(..., description="Short description of the object.")
    location: str = Field(..., description="E.g., 'center', 'top-left', 'bottom-right foreground'.")
    relationship: Optional[str] = Field(
        None, description="Describe the relationship between the object and the other objects in the image."
    )
    relative_size: Optional[str] = Field(None, description="E.g., 'small', 'medium', 'large within frame'.")
    shape_and_color: Optional[str] = Field(None, description="Describe the basic shape and dominant color.")
    texture: Optional[str] = Field(None, description="E.g., 'smooth', 'rough', 'metallic', 'furry'.")
    appearance_details: Optional[str] = Field(None, description="Any other notable visual details.")
    # If cluster of object
    number_of_objects: Optional[int] = Field(None, description="The number of objects in the cluster.")
    # Human-specific fields
    pose: Optional[str] = Field(None, description="Describe the body position.")
    expression: Optional[str] = Field(None, description="Describe facial expression.")
    clothing: Optional[str] = Field(None, description="Describe attire.")
    action: Optional[str] = Field(None, description="Describe the action of the human.")
    gender: Optional[str] = Field(None, description="Describe the gender of the human.")
    skin_tone_and_texture: Optional[str] = Field(None, description="Describe the skin tone and texture.")
    orientation: Optional[str] = Field(None, description="Describe the orientation of the human.")


class LightingDetails(BaseModel):
    conditions: str = Field(
        ..., description="E.g., 'bright daylight', 'dim indoor', 'studio lighting', 'golden hour'."
    )
    direction: str = Field(..., description="E.g., 'front-lit', 'backlit', 'side-lit from left'.")
    shadows: Optional[str] = Field(None, description="Describe the presence of shadows.")


class AestheticsDetails(BaseModel):
    composition: str = Field(..., description="E.g., 'rule of thirds', 'symmetrical', 'centered', 'leading lines'.")
    color_scheme: str = Field(
        ..., description="E.g., 'monochromatic blue', 'warm complementary colors', 'high contrast'."
    )
    mood_atmosphere: str = Field(..., description="E.g., 'serene', 'energetic', 'mysterious', 'joyful'.")


class PhotographicCharacteristicsDetails(BaseModel):
    depth_of_field: str = Field(..., description="E.g., 'shallow', 'deep', 'bokeh background'.")
    focus: str = Field(..., description="E.g., 'sharp focus on subject', 'soft focus', 'motion blur'.")
    camera_angle: str = Field(..., description="E.g., 'eye-level', 'low angle', 'high angle', 'dutch angle'.")
    lens_focal_length: str = Field(..., description="E.g., 'wide-angle', 'telephoto', 'macro', 'fisheye'.")


class TextRender(BaseModel):
    text: str = Field(..., description="The text content.")
    location: str = Field(..., description="E.g., 'center', 'top-left', 'bottom-right foreground'.")
    size: str = Field(..., description="E.g., 'small', 'medium', 'large within frame'.")
    color: str = Field(..., description="E.g., 'red', 'blue', 'green'.")
    font: str = Field(..., description="E.g., 'realistic', 'cartoonish', 'minimalist'.")
    appearance_details: Optional[str] = Field(None, description="Any other notable visual details.")


class ImageAnalysis(BaseModel):
    short_description: str = Field(..., description="A concise summary of the image content, 200 words maximum.")
    objects: List[ObjectDescription] = Field(..., description="List of prominent foreground/midground objects.")
    background_setting: str = Field(
        ...,
        description="Describe the overall environment, setting, or background, including any notable background elements.",
    )
    lighting: LightingDetails = Field(..., description="Details about the lighting.")
    aesthetics: AestheticsDetails = Field(..., description="Details about the image aesthetics.")
    photographic_characteristics: Optional[PhotographicCharacteristicsDetails] = Field(
        None, description="Details about photographic characteristics."
    )
    style_medium: Optional[str] = Field(None, description="Identify the artistic style or medium.")
    text_render: Optional[List[TextRender]] = Field(None, description="List of text renders in the image.")
    context: str = Field(..., description="Provide any additional context that helps understand the image better.")
    artistic_style: Optional[str] = Field(
        None, description="describe specific artistic characteristics, 3 words maximum."
    )


def get_output_schema() -> dict:
    return {
        "properties": {
            "short_description": {"type": "STRING"},
            "objects": {
                "items": {
                    "properties": {
                        "description": {"type": "STRING"},
                        "location": {"type": "STRING"},
                        "relationship": {"type": "STRING"},
                        "relative_size": {"type": "STRING"},
                        "shape_and_color": {"type": "STRING"},
                        "texture": {"nullable": True, "type": "STRING"},
                        "appearance_details": {"nullable": True, "type": "STRING"},
                        "number_of_objects": {"nullable": True, "type": "INTEGER"},
                        "pose": {"nullable": True, "type": "STRING"},
                        "expression": {"nullable": True, "type": "STRING"},
                        "clothing": {"nullable": True, "type": "STRING"},
                        "action": {"nullable": True, "type": "STRING"},
                        "gender": {"nullable": True, "type": "STRING"},
                        "skin_tone_and_texture": {"nullable": True, "type": "STRING"},
                        "orientation": {"nullable": True, "type": "STRING"},
                    },
                    "required": [
                        "description",
                        "location",
                        "relationship",
                        "relative_size",
                        "shape_and_color",
                        "texture",
                        "appearance_details",
                        "number_of_objects",
                        "pose",
                        "expression",
                        "clothing",
                        "action",
                        "gender",
                        "skin_tone_and_texture",
                        "orientation",
                    ],
                    "type": "OBJECT",
                },
                "type": "ARRAY",
            },
            "background_setting": {"type": "STRING"},
            "lighting": {
                "properties": {
                    "conditions": {"type": "STRING"},
                    "direction": {"type": "STRING"},
                    "shadows": {"nullable": True, "type": "STRING"},
                },
                "required": ["conditions", "direction", "shadows"],
                "type": "OBJECT",
            },
            "aesthetics": {
                "properties": {
                    "composition": {"type": "STRING"},
                    "color_scheme": {"type": "STRING"},
                    "mood_atmosphere": {"type": "STRING"},
                },
                "required": ["composition", "color_scheme", "mood_atmosphere"],
                "type": "OBJECT",
            },
            "photographic_characteristics": {
                "nullable": True,
                "properties": {
                    "depth_of_field": {"type": "STRING"},
                    "focus": {"type": "STRING"},
                    "camera_angle": {"type": "STRING"},
                    "lens_focal_length": {"type": "STRING"},
                },
                "required": [
                    "depth_of_field",
                    "focus",
                    "camera_angle",
                    "lens_focal_length",
                ],
                "type": "OBJECT",
            },
            "style_medium": {"type": "STRING"},
            "text_render": {
                "items": {
                    "properties": {
                        "text": {"type": "STRING"},
                        "location": {"type": "STRING"},
                        "size": {"type": "STRING"},
                        "color": {"type": "STRING"},
                        "font": {"type": "STRING"},
                        "appearance_details": {"nullable": True, "type": "STRING"},
                    },
                    "required": [
                        "text",
                        "location",
                        "size",
                        "color",
                        "font",
                        "appearance_details",
                    ],
                    "type": "OBJECT",
                },
                "type": "ARRAY",
            },
            "context": {"type": "STRING"},
            "artistic_style": {"type": "STRING"},
        },
        "required": [
            "short_description",
            "objects",
            "background_setting",
            "lighting",
            "aesthetics",
            "photographic_characteristics",
            "style_medium",
            "text_render",
            "context",
            "artistic_style",
        ],
        "type": "OBJECT",
    }


json_schema_full = """1.  `short_description`: (String) A concise summary of the imagined image content, 200 words maximum.
2.  `objects`: (Array of Objects) List a maximum of 5 prominent objects. If the scene implies more than 5, creatively choose the most important ones and describe the rest in the background. For each object, include:
    * `description`: (String) A detailed description of the imagined object, 100 words maximum.
    * `location`: (String) E.g., "center", "top-left", "bottom-right foreground".
    * `relative_size`: (String) E.g., "small", "medium", "large within frame". (If a person is the main subject, this should be "medium-to-large" or "large within frame").
    * `shape_and_color`: (String) Describe the basic shape and dominant color.
    * `texture`: (String) E.g., "smooth", "rough", "metallic", "furry".
    * `appearance_details`: (String) Any other notable visual details.
    * `relationship`: (String) Describe the relationship between the object and the other objects in the image.
    * `orientation`: (String) Describe the orientation or positioning of the object, e.g., "upright", "tilted 45 degrees", "horizontal", "vertical", "facing left", "facing right", "upside down", "lying on its side".
    * If the object is a human or a human-like object, include the following:
        * `pose`: (String) Describe the body position.
        * `expression`: (String) Describe facial expression and emotion. E.g., "winking", "joyful", "serious", "surprised", "calm".
        * `clothing`: (String) Describe attire.
        * `action`: (String) Describe the action of the human.
        * `gender`: (String) Describe the gender of the human.
        * `skin_tone_and_texture`: (String) Describe the skin tone and texture.
    * If the object is a cluster of objects, include the following:
        * `number_of_objects`: (Integer) The number of objects in the cluster.
3.  `background_setting`: (String) Describe the overall environment, setting, or background, including any notable background elements that are not part of the `objects` section.
4.  `lighting`: (Object)
    * `conditions`: (String) E.g., "bright daylight", "dim indoor", "studio lighting", "golden hour".
    * `direction`: (String) E.g., "front-lit", "backlit", "side-lit from left".
    * `shadows`: (String) Describe the presence and quality of shadows, e.g., "long, soft shadows", "sharp, defined shadows", "minimal shadows".
5.  `aesthetics`: (Object)
    * `composition`: (String) E.g., "rule of thirds", "symmetrical", "centered", "leading lines". If people are the main subject, specify the shot type, e.g., "medium shot", "close-up", "portrait composition".
    * `color_scheme`: (String) E.g., "monochromatic blue", "warm complementary colors", "high contrast".
    * `mood_atmosphere`: (String) E.g., "serene", "energetic", "mysterious", "joyful".
6.  `photographic_characteristics`: (Object)
    * `depth_of_field`: (String) E.g., "shallow", "deep", "bokeh background".
    * `focus`: (String) E.g., "sharp focus on subject", "soft focus", "motion blur".
    * `camera_angle`: (String) E.g., "eye-level", "low angle", "high angle", "dutch angle".
    * `lens_focal_length`: (String) E.g., "wide-angle", "telephoto", "macro", "fisheye". (If the main subject is a person, prefer "standard lens (e.g., 35mm-50mm)" or "portrait lens (e.g., 50mm-85mm)" to ensure they are framed more closely. Avoid "wide-angle" for people unless specified).
7.  `style_medium`: (String) Identify the artistic style or medium based on the user's prompt or creative interpretation (e.g., "photograph", "oil painting", "watercolor", "3D render", "digital illustration", "pencil sketch").
8.  `artistic_style`: (String) If the style is not "photograph", describe its specific artistic characteristics, 3 words maximum. (e.g., "impressionistic, vibrant, textured" for an oil painting).
9.  `context`: (String) Provide a general description of the type of image this would be. For example: "This is a concept for a high-fashion editorial photograph intended for a magazine spread," or "This describes a piece of concept art for a fantasy video game."
10. `text_render`: (Array of Objects) By default, this array should be empty (`[]`). Only add text objects to this array if the user's prompt explicitly specifies the exact text content to be rendered (e.g., user asks for "a poster with the title 'Cosmic Dream'"). Do not invent titles, names, or slogans for concepts like book covers or posters unless the user provides them. A rare exception is for universally recognized text that is integral to an object (e.g., the word 'STOP' on a 'stop sign'). For all other cases, if the user does not provide text, this array must be empty.
    * `text`: (String) The exact text content provided by the user. NEVER use generic placeholders.
    * `location`: (String) E.g., "center", "top-left", "bottom-right foreground".
    * `size`: (String) E.g., "medium", "large", "large within frame".
    * `color`: (String) E.g., "red", "blue", "green".
    * `font`: (String) E.g., "realistic", "cartoonish", "minimalist", "serif typeface".
    * `appearance_details`: (String) Any other notable visual details."""

@cache
def get_instructions(mode: str) -> Tuple[str, str]:

    system_prompts = {}

    system_prompts["Caption"] = f"""You are a meticulous and perceptive Visual Art Director working for a leading Generative AI company. Your expertise lies in analyzing images and extracting detailed, structured information.
Your primary task is to analyze provided images and generate a comprehensive JSON object describing them. Adhere strictly to the following structure and guidelines:
The output MUST be ONLY a valid JSON object. Do not include any text before or after the JSON object (e.g., no "Here is the JSON:", no explanations, no apologies).
IMPORTANT: When describing human body parts, positions, or actions, always describe them from the PERSON'S OWN PERSPECTIVE, not from the observer's viewpoint. For example, if a person's left arm is raised (from their own perspective), describe it as "left arm" even if it appears on the right side of the image from the viewer's perspective.
The JSON object must contain the following keys precisely:
{json_schema_full}
Ensure the information within the JSON is accurate, detailed where specified, and avoids redundancy between fields.
"""
        
    system_prompts["Generate"] = f"""You are a visionary and creative Visual Art Director at a leading Generative AI company.
Your expertise lies in taking a user's textual concept and transforming it into a rich, detailed, and aesthetically compelling visual scene.
Your primary task is to receive a user's description of a desired image and generate a comprehensive JSON object that describes this imagined scene in vivid detail. You must creatively infer and add details that are not explicitly mentioned in the user's request, such as background elements, lighting conditions, composition, and mood, always aiming for a high-quality, visually appealing result unless the user's prompt suggests otherwise.
Adhere strictly to the following structure and guidelines:
The output MUST be ONLY a valid JSON object. Do not include any text before or after the JSON object (e.g., no "Here is the JSON:", no explanations, no apologies).
IMPORTANT: When describing human body parts, positions, or actions, always describe them from the PERSON'S OWN PERSPECTIVE, not from the observer's viewpoint. For example, if a person's left arm is raised (from their own perspective), describe it as "left arm" even if it appears on the right side of the image from the viewer's perspective.
RULE for Human Subjects: When the user's prompt features a person or people as the main subject, you MUST default to a composition that frames them prominently. Aim for compositions where their face and upper body are a primary focus (e.g., 'medium shot', 'close-up'). Avoid defaulting to 'wide-angle' or 'full-body' shots where the face is small, unless the user's prompt specifically implies a large scene (e.g., "a person standing on a mountain").
Unless the user's prompt explicitly requests a different style (e.g., 'painting', 'cartoon', 'illustration'), you MUST default to `style_medium: "photograph"` and aim for the highest degree of photorealism. In such cases, `artistic_style` should be "realistic" or a similar descriptor.
The JSON object must contain the following keys precisely:
{json_schema_full}
Ensure the information within the JSON is detailed, creative, internally consistent, and avoids redundancy between fields."""

    system_prompts["RefineA"] = f"""You are a Meticulous Visual Editor and Senior Art Director at a leading Generative AI company.
Your expertise is in refining and modifying existing visual concepts based on precise feedback.
Your primary task is to receive an existing JSON object that describes a visual scene, along with a textual instruction for how to change it. You must then generate a new, updated JSON object that perfectly incorporates the requested changes.
Adhere strictly to the following structure and guidelines:
1.  **Input:** You will receive two pieces of information: an existing JSON object and a textual instruction.
2.  **Output:** Your output MUST be ONLY a single, valid JSON object in the specified schema. Do not include any text before or after the JSON object.
3.  **Modification Logic:**
    * Carefully parse the user's textual instruction to understand the desired changes.
    * Modify ONLY the fields in the JSON that are directly or logically affected by the instruction.
    * All other fields not relevant to the change must be copied exactly from the original JSON. Do not alter or omit them.
4.  **Holistic Consistency (IMPORTANT):** Changes in one field must be logically reflected in others. For example:
    * If the instruction is to "change the background to a snowy forest," you must update the `background_setting` field, and also update the `short_description` to mention the new setting. The `mood_atmosphere` might also need to change to "serene" or "wintry."
    * If the instruction is to "add the text 'WINTER SALE' at the top," you must add a new entry to the `text_render` array.
    * If the instruction is to "make the person smile," you must update the `expression` field for that object and potentially update the overall `mood_atmosphere`.
5.  **Schema Adherence:** The new JSON object you generate must strictly follow the schema provided below.
The JSON object must contain the following keys precisely:
{json_schema_full}"""

    system_prompts["RefineB"] = f"""You are an advanced Multimodal Visual Specialist at a leading Generative AI company.
Your unique expertise is in analyzing and editing visual concepts by processing an image, its corresponding JSON metadata, and textual feedback simultaneously.
Your primary task is to receive three inputs: an existing image, its descriptive JSON object, and a textual instruction for a modification. You must use the image as the primary source of truth to understand the context of the requested change and then generate a new, updated JSON object that accurately reflects that change.
Adhere strictly to the following structure and guidelines:
1.  **Inputs:** You will receive an image, an existing JSON object, and a textual instruction.
2.  **Visual Grounding (IMPORTANT):** The provided image is the ground truth. Use it to visually verify the contents of the scene and to understand the context of the user's edit instruction. For example, if the instruction is "make the car blue," visually locate the car in the image to inform your edits to the JSON.
3.  **Output:** Your output MUST be ONLY a single, valid JSON object in the specified schema. Do not include any text before or after the JSON object.
4.  **Modification Logic:**
    * Analyze the user's textual instruction in the context of what you see in the image.
    * Modify ONLY the fields in the JSON that are directly or logically affected by the instruction.
    * All other fields not relevant to the change must be copied exactly from the original JSON.
5.  **Holistic Consistency:** Changes must be reflected logically across the JSON, consistent with a potential visual change to the image. For instance, changing the lighting from 'daylight' to 'golden hour' should not only update the `lighting` object but also the `mood_atmosphere`, `shadows`, and the `short_description`.
6.  **Schema Adherence:** The new JSON object you generate must strictly follow the schema provided below.
The JSON object must contain the following keys precisely:
{json_schema_full}"""

    system_prompts["InspireA"] = f"""You are a highly skilled Creative Director for Visual Adaptation at a leading Generative AI company.
Your expertise lies in using an existing image as a visual reference to create entirely new scenes. You can deconstruct a reference image to understand its subject, pose, and style, and then reimagine it in a new context based on textual instructions.
Your primary task is to receive a reference image and a textual instruction. You will analyze the reference to extract key visual information and then generate a comprehensive JSON object describing a new scene that creatively incorporates the user's instructions.
Adhere strictly to the following structure and guidelines:
1.  **Inputs:** You will receive a reference image and a textual instruction. You will NOT receive a starting JSON.
2.  **Core Logic (Analyze and Synthesize):**
    * **Analyze:** First, deeply analyze the provided reference image. Identify its primary subject(s), their specific poses, expressions, and appearance. Also note the overall composition, lighting style, and artistic medium.
    * **Synthesize:** Next, interpret the textual instruction to understand what elements to keep from the reference and what to change. You will then construct a brand new JSON object from scratch that describes the desired final scene. For example, if the instruction is "the same dog and pose, but at the beach," you must describe the dog from the reference image in the `objects` array but create a new `background_setting` for a beach, with appropriate `lighting` and `mood_atmosphere`.
3.  **Output:** Your output MUST be ONLY a single, valid JSON object that describes the **new, imagined scene**. Do not describe the original reference image.
4.  **Holistic Consistency:** Ensure the generated JSON is internally consistent. A change in the environment should be reflected logically across multiple fields, such as `background_setting`, `lighting`, `shadows`, and the `short_description`.
5.  **Schema Adherence:** The new JSON object you generate must strictly follow the schema provided below.
Unless the user's prompt explicitly requests a different style (e.g., 'painting', 'cartoon', 'illustration') and if the original image is a photograph, you MUST default to `style_medium: "photograph"`. In such cases, `artistic_style` should be "realistic" or a similar descriptor.
The JSON object must contain the following keys precisely:
{json_schema_full}"""

    system_prompts["InspireB"] = system_prompts["Caption"]


    final_prompts = {}

    final_prompts["Generate"] = "Generate a detailed JSON object, adhering to the expected schema, for an imagined scene based on the following request: {user_prompt}."

    final_prompts["RefineA"] = """
        [EXISTING JSON]:
        {json_data}
        [EDIT INSTRUCTIONS]:
        {user_prompt}
        [TASK]:
        Generate the new, updated JSON object that incorporates the edit instructions. Follow all system rules for modification, consistency, and formatting.
        """

    final_prompts["RefineB"] = """
        [EXISTING JSON]:
        {json_data}
        [EDIT INSTRUCTIONS]:
        {user_prompt}
        [TASK]:
        Analyze the provided image and its contextual JSON. Then, generate the new, updated JSON object that incorporates the edit instructions. Follow all your system rules for visual analysis, modification, and consistency.
        """

    final_prompts["InspireA"] = """
        [EDIT INSTRUCTIONS]:
        {user_prompt}
        [TASK]:
        Use the provided image as a visual reference only. Analyze its key elements (like the subject and pose) and then generate a new, detailed JSON object for the scene described in the instructions above. Do not describe the reference image itself; describe the new scene. Follow all of your system rules.
        """

    final_prompts["Caption"] = "Analyze the provided image and generate the detailed JSON object as specified in your instructions."
    final_prompts["InspireB"] = final_prompts["Caption"]


    return system_prompts.get(mode, ""), final_prompts.get(mode, "")




def validate_json(json_data: str, verbose: bool = False) -> dict:
    if verbose:
        print(f"🔍 [validate_json] Validating JSON response against schema")
    
    # Strip markdown code blocks if present (some models wrap JSON in ```json ... ```)
    if isinstance(json_data, str):
        json_data = json_data.strip()
        if json_data.startswith("```json"):
            json_data = json_data[7:]  # Remove ```json
        elif json_data.startswith("```"):
            json_data = json_data[3:]  # Remove ```
        if json_data.endswith("```"):
            json_data = json_data[:-3]  # Remove trailing ```
        json_data = json_data.strip()
        
        if verbose:
            print(f"   Cleaned JSON length: {len(json_data)} chars")
    
    try:
        ia = ImageAnalysis.model_validate_json(json_data, strict=False)  # Use strict=False for more lenient validation
        result = ia.model_dump(exclude_none=True)
        
        if verbose:
            print(f"✅ [validate_json] Validation successful, {len(result)} top-level fields")
        
        return result
    except Exception as e:
        # If validation fails, try to parse as dict and add missing fields
        if verbose:
            print(f"⚠️  [validate_json] Validation failed, attempting to fix: {str(e)[:100]}")
        
        try:
            # Parse JSON string to dict
            data_dict = json.loads(json_data) if isinstance(json_data, str) else json_data
            
            # Add missing required fields with defaults
            if 'objects' in data_dict:
                for obj in data_dict['objects']:
                    if 'relationship' not in obj:
                        obj['relationship'] = "standalone"  # Default value
            
            # Try validation again
            ia = ImageAnalysis.model_validate(data_dict, strict=False)
            result = ia.model_dump(exclude_none=True)
            
            if verbose:
                print(f"✅ [validate_json] Validation successful after fixes, {len(result)} top-level fields")
            
            return result
        except Exception as e2:
            print(f"❌ [validate_json] Validation failed even after fixes: {str(e2)}")
            raise e  # Raise original error


def validate_structured_prompt_str(structured_prompt_str: str) -> str:
    ia = ImageAnalysis.model_validate_json(structured_prompt_str, strict=True)
    c = ia.model_dump(exclude_none=True)
    return json.dumps(c)





# resize an input image to have a specific number of pixels (1,048,576 or 1024×1024)
# while maintaining a certain aspect ratio and granularity (output width and height must be multiples of this number).
def resize_image_by_num_pixels(
    image: Image.Image, pixel_number: int = 1048576, granularity_val: int = 64, target_ratio: float = 0.0, verbose: bool = False
) -> Image.Image:
    if verbose:
        print(f"🔧 [resize_image_by_num_pixels] Original size: {image.size[0]}x{image.size[1]} ({image.size[0] * image.size[1]:,} pixels)")
    
    if target_ratio != 0.0:
        ratio = target_ratio
    else:
        ratio = image.size[0] / image.size[1]
    width = int((pixel_number * ratio) ** 0.5)
    width = width - (width % granularity_val)
    height = int(pixel_number / width)
    height = height - (height % granularity_val)
    
    if verbose:
        print(f"🔧 [resize_image_by_num_pixels] Resized to: {width}x{height} ({width * height:,} pixels)")
    
    return image.resize((width, height))


def infer_with_bedrock(
    client: boto3.client,
    final_prompt: str,
    system_prompt: str,
    top_p: float,
    temperature: float,
    max_tokens: int,
    seed: int = 42,
    image: Optional[Image.Image] = None,
    model: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    verbose: bool = False,
) -> Tuple[str, dict]:
    """
    Calls AWS Bedrock with Claude 3.5 Sonnet and returns the raw JSON response.
    Args:
        client: Boto3 Bedrock Runtime client
        final_prompt: The text prompt to send to Claude
        system_prompt: The system instruction for Claude
        top_p: Top-p sampling parameter
        temperature: Temperature for sampling
        max_tokens: Maximum tokens to generate
        seed: Random seed (not used by Bedrock)
        image: Optional PIL Image to include
        model: The Bedrock model ID to use
        verbose: Enable verbose logging
    Returns:
        Raw JSON response text from Claude
    """
    if verbose:
        print(f"\n🚀 [infer_with_bedrock] Starting API call")
        print(f"   Model: {model}")
        print(f"   Temperature: {temperature}, Top-p: {top_p}, Max tokens: {max_tokens}")
        print(f"   Has image: {image is not None}")
        print(f"   Prompt length: {len(final_prompt)} chars")
        print(f"   System prompt length: {len(system_prompt)} chars")
    
    # Build the message content for Bedrock Converse API
    content = []
    
    # Add image if provided
    if image:
        if verbose:
            print(f"   Processing image: {image.size[0]}x{image.size[1]}")
        
        # Convert image to base64
        image = image.convert("RGB")
        less_then = 262144
        if image.size[0] * image.size[1] > less_then:
            if verbose:
                print(f"   Image too large, resizing...")
            image = resize_image_by_num_pixels(
                image, pixel_number=less_then, granularity_val=1, target_ratio=0.0, verbose=verbose
            )
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        if verbose:
            print(f"   Image encoded: {len(image_bytes):,} bytes")
        
        # Bedrock Converse API format for images
        content.append({
            "image": {
                "format": "jpeg",
                "source": {
                    "bytes": image_bytes  # Use bytes directly, not base64
                }
            }
        })
    
    # Add text prompt - Bedrock Converse API format
    content.append({
        "text": final_prompt
    })
    
    # Build the request body for Bedrock Converse API
    request_body = {
        "modelId": model,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "system": [
            {
                "text": system_prompt
            }
        ],
        "inferenceConfig": {
            "temperature": temperature,
            "topP": top_p,
            "maxTokens": max_tokens
        }
    }
    
    if verbose:
        print(f"   Calling Bedrock Converse API...")
    
    # Call Bedrock Converse API
    response = client.converse(**request_body)
    
    # Extract token usage information
    usage = response.get('usage', {})
    input_tokens = usage.get('inputTokens', 0)
    output_tokens = usage.get('outputTokens', 0)
    total_tokens = usage.get('totalTokens', 0)
    
    # Print token usage
    print(f"📊 Token Usage - Model: {model}")
    print(f"   Input tokens:  {input_tokens:,}")
    print(f"   Output tokens: {output_tokens:,}")
    print(f"   Total tokens:  {total_tokens:,}")
    
    # Extract the response text
    response_text = response['output']['message']['content'][0]['text']
    
    if verbose:
        print(f"   Response length: {len(response_text)} chars")
        print(f"✅ [infer_with_bedrock] API call completed")
    
    # Return both response text and usage info
    return response_text, usage


def get_default_negative_prompt(existing_json: dict) -> str:
    negative_prompt = ""
    style_medium = existing_json.get("style_medium", "").lower()
    if style_medium in ["photograph", "photography", "photo"]:
        negative_prompt = """{'style_medium': 'digital illustration', 'artistic_style': 'non-realistic'}"""
    return negative_prompt

def clean_json(caption, verbose: bool = False):
    if verbose:
        print(f"🧹 [clean_json] Cleaning and preparing caption")
    
    caption['pickascore']=1.0
    caption['aesthetic_score']=10.0    
    caption = prepare_clean_caption(caption, verbose=verbose)
    
    if verbose:
        print(f"✅ [clean_json] Caption cleaned, length: {len(caption)} chars")
    
    return caption

def parse_aesthetic_score(record: dict) -> str:
    ae = record["aesthetic_score"]
    if ae < 5.5:
        return "very low"
    elif ae < 6:
        return "low"
    elif ae < 7:
        return "medium"
    elif ae < 7.6:
        return "high"
    else:
        return "very high"

def parse_pickascore(record: dict) -> str:
    ps = record["pickascore"]
    if ps < 0.78:
        return "very low"
    elif ps < 0.82:
        return "low"
    elif ps < 0.87:
        return "medium"
    elif ps < 0.91:
        return "high"
    else:
        return "very high"

def prepare_clean_caption(record: dict, verbose: bool = False) -> str:
    if verbose:
        print(f"📝 [prepare_clean_caption] Preparing clean caption from record")
    
    def keep(p, k, v):
        is_none = v is None
        is_empty_string = isinstance(v, str) and v == ""
        is_empty_dict = isinstance(v, dict) and not v
        is_empty_list = isinstance(v, list) and not v
        is_nan = isinstance(v, float) and math.isnan(v)   
        if is_none or is_empty_string or is_empty_list or is_empty_dict or is_nan:
            return False
        return True

    try:
        
        scores = {}
        if 'pickascore' in record:
            scores["preference_score"] = parse_pickascore(record)
        if 'aesthetic_score' in record:
            scores["aesthetic_score"] = parse_aesthetic_score(record)        

        if verbose and scores:
            print(f"   Added scores: {scores}")

        # Create structured caption dict of original values
        fields=[
            "short_description",
            "objects",
            "background_setting",
            "lighting",
            "aesthetics",
            "photographic_characteristics",
            "style_medium",
            "text_render",
            "context",
            "artistic_style",
            ]

        original_caption_dict = {f:record[f] for f in fields if f in record}
        
        if verbose:
            print(f"   Original fields: {len(original_caption_dict)}")

        # filter empty values recursivly (i.e. None, "", {}, [], float("nan"))
        clean_caption_dict = remap(original_caption_dict, visit=keep)
        
        if verbose:
            print(f"   After filtering empty values: {len(clean_caption_dict)} fields")

        # Set aesthetics scores
        if "aesthetics" not in clean_caption_dict:
            if len(scores)>0:
                clean_caption_dict["aesthetics"] = scores
        else:
            clean_caption_dict["aesthetics"].update(scores)

        # Dumps clean structured caption as minimal json string (i.e. no newlines\whitespaces seps)
        clean_caption_str = ujson.dumps(clean_caption_dict, escape_forward_slashes=False)
        
        if verbose:
            print(f"✅ [prepare_clean_caption] Caption prepared successfully")
        
        return clean_caption_str
    except Exception as ex:
        print("Error: ", ex)
        raise ex

def json_promptify(
    client: boto3.client,
    base_model_id: str,
    vlm_model_id: str,
    top_p: float,
    temperature: float,
    max_tokens: int,
    user_prompt: Optional[str] = None,
    existing_json: Optional[str] = None,
    image: Optional[Image.Image] = None,
    seed: int = 42,
    verbose: bool = False,
) -> str:
    if verbose:
        print(f"\n{'='*80}")
        print(f"🎯 [json_promptify] Starting JSON prompt generation")
        print(f"   User prompt: {user_prompt[:100] if user_prompt else 'None'}...")
        print(f"   Has existing JSON: {existing_json is not None}")
        print(f"   Has image: {image is not None}")
    
    # Determine mode and select appropriate model
    if existing_json:
        # make sure aesthetic scores are not in the existing json (will be added later)
        existing_json = json.loads(existing_json)
        if "aesthetics" in existing_json:
            existing_json["aesthetics"].pop("aesthetic_score", None)
            existing_json["aesthetics"].pop("preference_score", None)
        existing_json = json.dumps(existing_json)

        if not user_prompt:
            raise ValueError("user_prompt is required if existing_json is provided")

        if image:
            # RefineB: image + JSON + text → JSON (uses VLM)
            mode = "RefineB"
            model_id = vlm_model_id
            system_prompt, final_prompt = get_instructions(mode)
            final_prompt = final_prompt.format(user_prompt=user_prompt, json_data=existing_json)
        else:
            # RefineA: JSON + text → JSON (uses BASE)
            mode = "RefineA"
            model_id = base_model_id
            system_prompt, final_prompt = get_instructions(mode)
            final_prompt = final_prompt.format(user_prompt=user_prompt, json_data=existing_json)
    elif image and user_prompt:
        # InspireA: image + text → JSON (uses VLM)
        mode = "InspireA"
        model_id = vlm_model_id
        system_prompt, final_prompt = get_instructions(mode)
        final_prompt = final_prompt.format(user_prompt=user_prompt)
    elif image and not user_prompt:
        # Caption: image → JSON (uses VLM)
        mode = "Caption"
        model_id = vlm_model_id
        system_prompt, final_prompt = get_instructions(mode)
    else:
        # Generate: text → JSON (uses BASE)
        mode = "Generate"
        model_id = base_model_id
        system_prompt, final_prompt = get_instructions(mode)
        final_prompt = final_prompt.format(user_prompt=user_prompt)

    print(f"Mode: {mode} | Using model: {model_id}")
    
    if verbose:
        print(f"   Selected mode: {mode}")
        print(f"   Selected model: {model_id}")
    
    # infer_with_bedrock now returns (response_text, usage_dict)
    json_data, usage = infer_with_bedrock(
        client=client,
        model=model_id,
        final_prompt=final_prompt,
        system_prompt=system_prompt,
        seed=seed,
        image=image,
        top_p=top_p,
        temperature=temperature,
        max_tokens=max_tokens,
        verbose=verbose,
    )
    json_data = validate_json(json_data, verbose=verbose)
    clean_caption = clean_json(json_data, verbose=verbose)

    if verbose:
        print(f"✅ [json_promptify] JSON prompt generation completed")
        print(f"{'='*80}\n")

    # Return both clean caption and usage info for token tracking
    return clean_caption, usage, mode, model_id


class TokenTracker:
    """Track token usage across multiple API calls"""
    def __init__(self):
        self.calls = []
        self.total_input = 0
        self.total_output = 0
        self.total_tokens = 0
    
    def add(self, model: str, mode: str, input_tokens: int, output_tokens: int, total_tokens: int):
        self.calls.append({
            'model': model,
            'mode': mode,
            'input': input_tokens,
            'output': output_tokens,
            'total': total_tokens
        })
        self.total_input += input_tokens
        self.total_output += output_tokens
        self.total_tokens += total_tokens
    
    def print_summary(self):
        if not self.calls:
            return
        
        print("\n" + "=" * 80)
        print("📊 TOKEN USAGE SUMMARY")
        print("=" * 80)
        for i, call in enumerate(self.calls, 1):
            print(f"\nCall {i}: {call['mode']} mode")
            print(f"  Model: {call['model']}")
            print(f"  Input:  {call['input']:,} tokens")
            print(f"  Output: {call['output']:,} tokens")
            print(f"  Total:  {call['total']:,} tokens")
        
        print("\n" + "-" * 80)
        print(f"TOTAL ACROSS ALL CALLS:")
        print(f"  Input tokens:  {self.total_input:,}")
        print(f"  Output tokens: {self.total_output:,}")
        print(f"  Total tokens:  {self.total_tokens:,}")
        print("=" * 80 + "\n")


class BriaFiboBedrockPromptToJson(ModularPipelineBlocks):
    model_name = "BriaFibo"

    def __init__(self, region_name="us-east-1", verbose=False):
        super().__init__()
        # Initialize Bedrock client
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=region_name
        )
        
        # Get model IDs from environment variables with defaults
        # BASE_MODEL: For text-only operations (Generate, RefineA) - use efficient Nova
        self.base_model_id = os.getenv(
            'BASE_MODEL', 
            'us.amazon.nova-lite-v1:0'  # Fast, efficient Nova model for text-only
        )
        
        # VLM_MODEL: For vision operations (Caption, RefineB, InspireA) - use Claude
        self.vlm_model_id = os.getenv(
            'VLM_MODEL',
            'us.anthropic.claude-3-5-sonnet-20241022-v2:0'  # Claude for vision tasks
        )
        
        # Store verbose setting
        self.verbose = verbose
        
        # Initialize token tracker
        self.token_tracker = TokenTracker()
        
        print(f"Initialized with BASE_MODEL: {self.base_model_id}")
        print(f"Initialized with VLM_MODEL: {self.vlm_model_id}")
        if verbose:
            print(f"🔊 Verbose logging enabled")

    @property
    def expected_components(self):
        return []

    @property
    def inputs(self) -> List[InputParam]:
        task_input = InputParam("task", type_hint=str, required=False, description="VLM Task to execute")
        prompt_input = InputParam(
            "prompt",
            type_hint=str,
            required=False,
            description="Prompt to use",
        )
        image_input = InputParam(
            name="image", type_hint=Image.Image, required=False, description="image for inspiration mode"
        )
        json_prompt_input = InputParam(
            name="json_prompt", type_hint=str, required=False, description="JSON prompt to use"
        )
        sampling_top_p_input = InputParam(
            name="sampling_top_p", type_hint=float, required=False, description="Sampling top p", default=1.0
        )
        sampling_temperature_input = InputParam(
            name="sampling_temperature",
            type_hint=float,
            required=False,
            description="Sampling temperature",
            default=0.2,
        )
        sampling_max_tokens_input = InputParam(
            name="sampling_max_tokens", type_hint=int, required=False, description="Sampling max tokens", default=3000
        )
        verbose_input = InputParam(
            name="verbose", type_hint=bool, required=False, description="Enable verbose logging", default=False
        )
        return [
            task_input,
            prompt_input,
            image_input,
            json_prompt_input,
            sampling_top_p_input,
            sampling_temperature_input,
            sampling_max_tokens_input,
            verbose_input,
        ]

    @property
    def intermediate_inputs(self) -> List[InputParam]:
        return []

    @property
    def intermediate_outputs(self) -> List[OutputParam]:
        return [
            OutputParam(
                "json_prompt",
                type_hint=str,
                description="JSON prompt by the VLM",
            )
        ]

    def __call__(self, components, state: PipelineState) -> PipelineState:
        block_state = self.get_block_state(state)
        prompt = block_state.prompt
        image = block_state.image
        json_prompt = block_state.json_prompt
        
        # Get verbose setting from block_state or use instance default
        verbose = getattr(block_state, 'verbose', self.verbose)
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"🎬 [__call__] Pipeline execution started")
            print(f"   Prompt: {prompt[:100] if prompt else 'None'}...")
            print(f"   Has image: {image is not None}")
            print(f"   Has existing JSON: {json_prompt is not None}")
            print(f"{'='*80}")
        
        # Use the Bedrock client initialized in __init__
        # Pass both model IDs - json_promptify will select the appropriate one
        json_prompt, usage, mode, model_id = json_promptify(
            client=self.bedrock_client,
            base_model_id=self.base_model_id,
            vlm_model_id=self.vlm_model_id,
            top_p=block_state.sampling_top_p,
            temperature=block_state.sampling_temperature,
            max_tokens=block_state.sampling_max_tokens,
            user_prompt=prompt,
            existing_json=json_prompt,
            image=image,
            verbose=verbose,
        )
        
        # Track token usage
        self.token_tracker.add(
            model=model_id,
            mode=mode,
            input_tokens=usage.get('inputTokens', 0),
            output_tokens=usage.get('outputTokens', 0),
            total_tokens=usage.get('totalTokens', 0)
        )
        
        block_state.json_prompt = json_prompt
        self.set_block_state(state, block_state)
        
        # Print token usage summary at the end
        self.token_tracker.print_summary()
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"🏁 [__call__] Pipeline execution completed")
            print(f"{'='*80}\n")

        return components, state
