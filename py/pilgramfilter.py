import numpy as np
import torch
from PIL import Image

try:
    import pilgram
except ImportError:
    pilgram = None

try:
    import pilgram2
except ImportError:
    pilgram2 = None

PILGRAM_FILTERS = [
    "_1977",
    "aden",
    "brannan",
    "brooklyn",
    "clarendon",
    "earlybird",
    "gingham",
    "hudson",
    "inkwell",
    "kelvin",
    "lark",
    "lofi",
    "maven",
    "mayfair",
    "moon",
    "nashville",
    "perpetua",
    "reyes",
    "rise",
    "slumber",
    "stinson",
    "toaster",
    "valencia",
    "walden",
    "willow",
    "xpro2",
]

PILGRAM2_FILTERS = [
    "_1977",
    "aden",
    "ashby",
    "amaro",
    "brannan",
    "brooklyn",
    "charmes",
    "clarendon",
    "crema",
    "dogpatch",
    "earlybird",
    "gingham",
    "ginza",
    "hefe",
    "helena",
    "hudson",
    "inkwell",
    "juno",
    "kelvin",
    "lark",
    "lofi",
    "ludwig",
    "maven",
    "mayfair",
    "moon",
    "nashville",
    "perpetua",
    "poprocket",
    "reyes",
    "rise",
    "sierra",
    "skyline",
    "slumber",
    "stinson",
    "sutro",
    "toaster",
    "valencia",
    "walden",
    "willow",
    "xpro2",
]

class _BaseMingInstaFilterNode:
    CATEGORY = "image/filters"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "apply_filter"
    FILTERS = []
    MODULE = None
    MODULE_NAME = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "filter_name": (cls.FILTERS, {"default": "clarendon"}),
                "strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.05}),
            }
        }

    def _tensor_to_pil(self, image_tensor):
        arr = image_tensor.cpu().numpy()
        arr = np.clip(arr * 255.0, 0, 255).astype(np.uint8)
        if arr.shape[-1] == 1:
            arr = arr.squeeze(-1)
        return Image.fromarray(arr).convert("RGB")

    def _pil_to_tensor(self, image):
        arr = np.asarray(image).astype(np.float32) / 255.0
        return torch.from_numpy(arr)

    def apply_filter(self, image, filter_name, strength):
        if self.MODULE is None:
            raise ImportError(
                f"{self.MODULE_NAME} is not installed. Install this node's requirements.txt with ComfyUI's embedded Python, "
                "for example: python.exe -m pip install -r custom_nodes/ComfyUI-PilgramFilters/requirements.txt"
            )

        if not hasattr(self.MODULE, filter_name):
            raise ValueError(f"Unknown {self.MODULE_NAME} filter: {filter_name}")

        filter_fn = getattr(self.MODULE, filter_name)
        out = []

        for img in image:
            original = self._tensor_to_pil(img)
            filtered = filter_fn(original)

            if strength < 1.0:
                filtered = Image.blend(original, filtered, strength)

            out.append(self._pil_to_tensor(filtered))

        return (torch.stack(out, dim=0),)


class MingInstaFilterNode(_BaseMingInstaFilterNode):
    FILTERS = PILGRAM_FILTERS
    MODULE = pilgram
    MODULE_NAME = "pilgram"


class MingInstaFilterV2Node(_BaseMingInstaFilterNode):
    FILTERS = PILGRAM2_FILTERS
    MODULE = pilgram2
    MODULE_NAME = "pilgram2"


NODE_CLASS_MAPPINGS = {
    "MingInstaFilter": MingInstaFilterNode,
    "MingInstaFilter-v2": MingInstaFilterV2Node,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MingInstaFilter": "MingInstaFilter",
    "MingInstaFilter-v2": "MingInstaFilter-v2",
}
