from comfy_api.latest import io


class SamplerNameSelect(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        sampler_options = [
            "dpmpp_sde",
            "euler_ancestral",
            "seeds_2",
            "seeds_3",
            "euler",
        ]

        return io.Schema(
            node_id="SamplerNameSelect",
            category="sampling/custom_sampling/samplers",
            inputs=[
                io.Combo.Input(
                    "sampler_name",
                    options=sampler_options,
                )
            ],
            outputs=[io.String.Output("sampler_name")],
        )

    @classmethod
    def execute(cls, sampler_name: str) -> io.NodeOutput:
        return io.NodeOutput(sampler_name)


NODE_CLASS_MAPPINGS = {
    "ForsenKsampler STRING": SamplerNameSelect,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SamplerNameSelect": "ForsenKsampler STRING",
}
