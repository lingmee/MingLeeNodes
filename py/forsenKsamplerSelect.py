import comfy.samplers
import comfy.sample
from comfy_api.latest import ComfyExtension, io


class KSamplerSelectFiltered(io.ComfyNode):
    """Custom KSampler node with filtered sampler options"""

    @classmethod
    def define_schema(cls):
        # Define only the samplers you want in the dropdown
        ALLOWED_SAMPLERS = [
            "dpmpp_sde",
            "euler_ancestral",
            "seeds_2",
            "seeds_3",
            "euler"
        ]

        return io.Schema(
            node_id="KSamplerSelectFiltered",
            category="sampling/custom_sampling/samplers",
            inputs=[io.Combo.Input("sampler_name", options=ALLOWED_SAMPLERS)],
            outputs=[io.Sampler.Output()]
        )

    @classmethod
    def execute(cls, sampler_name) -> io.NodeOutput:
        sampler = comfy.samplers.sampler_object(sampler_name)
        return io.NodeOutput(sampler)

    get_sampler = execute


# Node mappings - required for ComfyUI to recognize the node
NODE_CLASS_MAPPINGS = {
    "KSamplerSelectFiltered": KSamplerSelectFiltered
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KSamplerSelectFiltered": "ForsenKsampler Combo"
}
