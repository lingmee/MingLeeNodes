from .py import forsen_datetime, forsen_count, preset_loader

NODE_CLASS_MAPPINGS = {
    **forsen_datetime.NODE_CLASS_MAPPINGS,
    **forsen_count.NODE_CLASS_MAPPINGS,
    **preset_loader.NODE_CLASS_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **forsen_datetime.NODE_DISPLAY_NAME_MAPPINGS,
    **forsen_count.NODE_DISPLAY_NAME_MAPPINGS,
    **preset_loader.NODE_DISPLAY_NAME_MAPPINGS,
}

WEB_DIRECTORY = "./web/js"

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]