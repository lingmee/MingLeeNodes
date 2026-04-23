import importlib
import os
import torch
import comfy.samplers
import comfy.sample
from nodes import common_ksampler, CLIPTextEncode
import torchvision.transforms.v2 as T
import torch.nn.functional as F
import logging
from PIL import Image
import numpy as np

import folder_paths

GLOBAL_MODELS_DIR = os.path.join(folder_paths.models_dir, "llm_gguf")

WEB_DIRECTORY = "./web/assets/js"

DEFAULT_INSTRUCTIONS = 'Generate a prompt from "{prompt}"'

try:
    Llama = importlib.import_module("llama_cpp_cuda").Llama
except ImportError:
    Llama = importlib.import_module("llama_cpp").Llama

# From https://github.com/BlenderNeko/ComfyUI_Noise/
def slerp(val, low, high):
    dims = low.shape

    low = low.reshape(dims[0], -1)
    high = high.reshape(dims[0], -1)

    low_norm = low/torch.norm(low, dim=1, keepdim=True)
    high_norm = high/torch.norm(high, dim=1, keepdim=True)

    low_norm[low_norm != low_norm] = 0.0
    high_norm[high_norm != high_norm] = 0.0

    omega = torch.acos((low_norm*high_norm).sum(1))
    so = torch.sin(omega)
    res = (torch.sin((1.0-val)*omega)/so).unsqueeze(1)*low + (torch.sin(val*omega)/so).unsqueeze(1) * high

    return res.reshape(dims)


class AnyType(str):
    """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

    def __ne__(self, __value: object) -> bool:
        return False


anytype = AnyType("*")

# Text Concatenate

class MingLee_Text_Concatenate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "delimiter": ("STRING", {"default": ", ", "multiline": True}),
                "clean_whitespace": (["true", "false"],),
            },
            "optional": {
                "text_a": ("STRING", {"forceInput": True}),
                "text_b": ("STRING", {"forceInput": True}),
                "text_c": ("STRING", {"forceInput": True}),
                "text_d": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "text_concatenate"

    CATEGORY = "ming/main"

    def text_concatenate(self, delimiter, clean_whitespace, **kwargs):
        text_inputs = []

        # Iterate over the received inputs in sorted order.
        for k in sorted(kwargs.keys()):
            v = kwargs[k]

            # Only process string input ports.
            if isinstance(v, str):
                if clean_whitespace == "true":
                    # Remove leading and trailing whitespace around this input.
                    v = v.strip()

                # Only use this input if it's a non-empty string.
                if v != "":
                    text_inputs.append(v)

        # Merge the inputs using the specified delimiter.
        merged_text = delimiter.join(text_inputs)

        return (merged_text,)


class Ming_LLM_Node:
    @classmethod
    def INPUT_TYPES(cls):
        model_options = []
        if os.path.isdir(GLOBAL_MODELS_DIR):
            gguf_files = [file for file in os.listdir(GLOBAL_MODELS_DIR) if file.endswith('.gguf')]
            model_options.extend(gguf_files)

        return {
            "required": {
                "prompt_1": ("STRING", {"multiline": True, "dynamicPrompts": True, "default": ""}),
                "prompt_2": ("STRING", {"multiline": True, "dynamicPrompts": True, "default": ""}),
                "prompt_3": ("STRING", {"multiline": True, "dynamicPrompts": True, "default": ""}),
                "enable_multiple": ("BOOLEAN", {"default": False}),  # Option to enable multiple inputs
                "random_seed": ("INT", {"default": 1234567890, "min": 0, "max": 0xffffffffffffffff}),
                "model": (model_options,),
                "max_tokens": ("INT", {"default": 4096, "min": 1, "max": 8192}),
                "apply_instructions": ("BOOLEAN", {"default": True}),
                "instructions": ("STRING", {"multiline": False, "default": DEFAULT_INSTRUCTIONS}),
            },
            "optional": {
                "adv_options_config": ("SRGADVOPTIONSCONFIG",),
            }
        }

    CATEGORY = "ming/main"
    FUNCTION = "main"
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("generated_prompt1", "generated_prompt2", "generated_prompt3", "original_prompt")

    def main(self, prompt_1, prompt_2, prompt_3, enable_multiple, random_seed, model, max_tokens, apply_instructions, instructions, adv_options_config=None):
        # Initialize outputs to None or empty strings
        output_1 = None
        output_2 = None
        output_3 = None

        model_path = os.path.join(GLOBAL_MODELS_DIR, model)

        if model.endswith(".gguf"):
            generate_kwargs = {'max_tokens': max_tokens, 'temperature': 1.0, 'top_p': 0.9, 'top_k': 50, 'repeat_penalty': 1.2}

            if adv_options_config:
                for option in ['temperature', 'top_p', 'top_k', 'repeat_penalty']:
                    if option in adv_options_config:
                        generate_kwargs[option] = adv_options_config[option]

            model_to_use = Llama(
                model_path=model_path,
                n_gpu_layers=-1,
                seed=random_seed,
                verbose=False,
                n_ctx=2048,
            )

            # Handle multiple prompt generation if 'enable_multiple' is True
            if enable_multiple:
                # Generate for prompt_1
                messages = [
                    {"role": "system", "content": f"You are a helpful assistant."},
                    {"role": "user", "content": instructions.replace("{prompt}", prompt_1) if "{prompt}" in instructions else f"{instructions} {prompt_1}"},
                ]
                llm_result_1 = model_to_use.create_chat_completion(messages, **generate_kwargs)
                output_1 = llm_result_1['choices'][0]['message']['content'].strip()

                # Generate for prompt_2
                messages = [
                    {"role": "system", "content": f"You are a helpful assistant."},
                    {"role": "user", "content": instructions.replace("{prompt}", prompt_2) if "{prompt}" in instructions else f"{instructions} {prompt_2}"},
                ]
                llm_result_2 = model_to_use.create_chat_completion(messages, **generate_kwargs)
                output_2 = llm_result_2['choices'][0]['message']['content'].strip()

                # Generate for prompt_3
                messages = [
                    {"role": "system", "content": f"You are a helpful assistant."},
                    {"role": "user", "content": instructions.replace("{prompt}", prompt_3) if "{prompt}" in instructions else f"{instructions} {prompt_3}"},
                ]
                llm_result_3 = model_to_use.create_chat_completion(messages, **generate_kwargs)
                output_3 = llm_result_3['choices'][0]['message']['content'].strip()

            else:
                # If not using multiple inputs, just generate for prompt_1 as default
                messages = [
                    {"role": "system", "content": f"You are a helpful assistant."},
                    {"role": "user", "content": instructions.replace("{prompt}", prompt_1) if "{prompt}" in instructions else f"{instructions} {prompt_1}"},
                ]
                llm_result = model_to_use.create_chat_completion(messages, **generate_kwargs)
                output_1 = llm_result['choices'][0]['message']['content'].strip()

        else:
            output_1 = "NOT A GGUF MODEL"
            output_2 = output_1
            output_3 = output_1

        # Return generated texts for all three prompts and the original prompt
        return output_1, output_2, output_3, prompt_1 if not enable_multiple else "Multiple prompts used"

class MingSamplerSelectA:
    @classmethod
    def INPUT_TYPES(s):
        all_samplers = ["dpm_adaptive", "dpmpp_2m", "ipdnm", "deis", "ddim", "uni_pc_bh2"]
        return {
            "required": {
                "filter_text": ("STRING", {"default": ""}),  # e.g. "dpmpp ipdnm"
                "samplers": ("LIST", {
                    "multiselect": True,
                    "choices": all_samplers
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "ming/main"

    def execute(self, filter_text, samplers):
        # Split on spaces, remove empty parts, and lowercase all
        filters = [f.strip().lower() for f in filter_text.split() if f.strip()]

        # Apply filter: keep samplers that match ANY of the filter words
        if filters:
            filtered = [s for s in samplers if any(f in s.lower() for f in filters)]
        else:
            filtered = samplers  # If no filter provided, return selected as-is

        return (", ".join(filtered),)


class MingSamplerSelectB:
    @classmethod
    def INPUT_TYPES(s):
        selected_samplers = ["euler", "dpm_adaptive", "deis", "ddim"]
        return {
            "required": {
                **{s: ("BOOLEAN", {"default": False}) for s in selected_samplers},
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "ming/main"

    def execute(self, **values):
        selected_values = [v for v in values if values[v]]
        selected_values_str = ", ".join(selected_values)

        return (selected_values_str,)

class MingSchedulerSelect:
    @classmethod
    def INPUT_TYPES(s):
        selected_schedulers = ["sgm_uniform", "simple", "beta", "ddim_uniform"]
        return {
            "required": {
                **{s: ("BOOLEAN", {"default": False}) for s in selected_schedulers},
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "ming/main"

    def execute(self, **values):
        selected_values = [v for v in values if values[v]]
        selected_values_str = ", ".join(selected_values)

        return (selected_values_str,)


class FlexibleImageGridCombiner:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"forceInput": True}),
                "columns": ("INT", {"default": 3, "min": 1, "max": 10}),
                "rows": ("INT", {"default": 2, "min": 1, "max": 10}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "combine"

    CATEGORY = "image"

    def combine(self, images, columns, rows):
        expected_count = columns * rows
        if len(images) != expected_count:
            raise ValueError(f"Grid is {columns}x{rows} = {expected_count}, but you provided {len(images)} images.")

        # Convert tensors to PIL images
        pil_images = [self.tensor_to_pil(img) for img in images]

        # Ensure all images are same size
        img_width, img_height = pil_images[0].size
        for img in pil_images:
            if img.size != (img_width, img_height):
                raise ValueError("All images must have the same dimensions.")

        # Create canvas
        canvas = Image.new("RGBA", (columns * img_width, rows * img_height))

        for idx, img in enumerate(pil_images):
            x = (idx % columns) * img_width
            y = (idx // columns) * img_height
            canvas.paste(img, (x, y))

        return (self.pil_to_tensor(canvas),)

    def tensor_to_pil(self, tensor_img):
        """Convert tensor (ComfyUI image) to PIL"""
        img = tensor_img[0]  # first in batch
        img = (img * 255).clip(0, 255).astype(np.uint8)
        return Image.fromarray(img)

    def pil_to_tensor(self, pil_img):
        """Convert PIL to tensor"""
        img = np.array(pil_img).astype(np.float32) / 255.0
        if img.ndim == 2:
            img = np.expand_dims(img, axis=-1)
        return np.expand_dims(img, axis=0)


# Text String Truncation

class MingTextTruncate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "truncate_by": (["characters", "words"],),
                "truncate_from": (["end", "beginning"],),
                "truncate_to": ("INT", {"default": 10, "min": -99999999, "max": 99999999, "step": 1}),
            },
            "optional": {
                "text_b": ("STRING", {"forceInput": True}),
                "text_c": ("STRING", {"forceInput": True}),
                "text_d": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("TEXT", "TEXT_B", "TEXT_C", "TEXT_D")
    FUNCTION = "truncate_string"

    CATEGORY = "ming/main"

    def truncate_string(self, text, truncate_by, truncate_from, truncate_to, text_b='', text_c='', text_d=''):
        return (
            self.truncate(text, truncate_to, truncate_from, truncate_by),
            self.truncate(text_b, truncate_to, truncate_from, truncate_by),
            self.truncate(text_c, truncate_to, truncate_from, truncate_by),
            self.truncate(text_d, truncate_to, truncate_from, truncate_by),
        )

    def truncate(self, string, max_length, mode='end', truncate_by='characters'):
        if mode not in ['beginning', 'end']:
            mode = "end"
        if truncate_by not in ['characters', 'words']:
            truncate_by = "characters"
        if truncate_by == 'characters':
            if mode == 'beginning':
                return string[:max_length] if max_length >= 0 else string[max_length:]
            else:
                return string[-max_length:] if max_length >= 0 else string[:max_length]
        words = string.split()
        if mode == 'beginning':
            return ' '.join(words[:max_length]) if max_length >= 0 else ' '.join(words[max_length:])
        else:
            return ' '.join(words[-max_length:]) if max_length >= 0 else ' '.join(words[:max_length])


NODE_CLASS_MAPPINGS = {
    "MingTextTruncate": MingTextTruncate,
    "Ming_LLM_Node": Ming_LLM_Node,
    "MingSamplerSelectA": MingSamplerSelectA,  # Add SamplerSelectHelperA
    "MingSamplerSelectB": MingSamplerSelectB,  # Add SamplerSelectHelperB
    "MingLee_Text_Concatenate": MingLee_Text_Concatenate,
    "MingSchedulerSelect": MingSchedulerSelect,
    "FlexibleImageGridCombiner": FlexibleImageGridCombiner,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MingTextTruncate": "MingTextTruncate",
    "Ming_LLM_Node": "Ming LLM Node",
    "MingSamplerSelectA": "MingSamplerSelectA",  # Name for SamplerSelectHelperA
    "MingSamplerSelectB": "MingSamplerSelectB",  # Name for SamplerSelectHelperB
    "MingSchedulerSelect": "MingSchedulerSelect",
    "MingLee_Text_Concatenate": "MingLee_Text_Concatenate",
    "FlexibleImageGridCombiner": "Ming Image Grid Combiner",
}
