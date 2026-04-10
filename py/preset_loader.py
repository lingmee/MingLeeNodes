import json
import os

class PresetLoader:

    def __init__(self):
        self.presets_file = os.path.join(os.path.dirname(__file__), "presets.json")
        self.presets = self._load_presets()

    def _load_presets(self):
        try:
            if os.path.exists(self.presets_file):
                with open(self.presets_file, 'r') as f:
                    data = json.load(f)
                    return data.get("presets", {})
            else:
                print(f"Warning: Presets file not found at {self.presets_file}")
                return {}
        except Exception as e:
            print(f"Error loading presets: {e}")
            return {}

    def get_preset_names(self):
        return list(self.presets.keys()) if self.presets else ["default"]

    @classmethod
    def INPUT_TYPES(cls):
        loader = PresetLoader()
        preset_names = loader.get_preset_names()

        return {
            "required": {
                "preset": (preset_names, {"default": preset_names[0] if preset_names else "default"}),
            }
        }

    RETURN_TYPES = ("STRING", "FLOAT", "FLOAT", "BOOLEAN", "STRING", "FLOAT", "INT", "FLOAT", "FLOAT")
    RETURN_NAMES = ("mode", "blend", "b", "apply_fourier", "multiscale_mode", "multiscale_strength", "threshold", "s", "force_gain")
    FUNCTION = "load_preset"
    CATEGORY = "presets"

    def load_preset(self, preset):
        # load and return values from preset
        if preset not in self.presets:
            print(f"Preset '{preset}' not found. Using first available preset.")
            preset = list(self.presets.keys())[0]

        preset_data = self.presets[preset]

        return (
            str(preset_data.get("mode", "default")),
            float(preset_data.get("blend", 0.0)),
            float(preset_data.get("b", 0.0)),
            bool(preset_data.get("apply_fourier", False)),
            str(preset_data.get("multiscale_mode", "default")),
            float(preset_data.get("multiscale_strength", 0.0)),
            int(preset_data.get("threshold", 0)),
            float(preset_data.get("s", 0.0)),
            float(preset_data.get("force_gain", 0.0))
        )

NODE_CLASS_MAPPINGS = {
    "PresetLoader": PresetLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PresetLoader": "Preset Loader"
}
