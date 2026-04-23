from .py import (
    forsen_datetime,
    forsen_count,
    preset_loader,
    forsenKsamplerSelect,
    ForsenKsamplerSimple,
    forsenprompt,
    ming_nodes,
    mingDiffLoad,
    mingSTRINGtimer,
    pilgramfilter,
)
NODE_CLASS_MAPPINGS = {
    **forsen_datetime.NODE_CLASS_MAPPINGS,
    **forsen_count.NODE_CLASS_MAPPINGS,
    **preset_loader.NODE_CLASS_MAPPINGS,
    **forsenKsamplerSelect.NODE_CLASS_MAPPINGS,
    **ForsenKsamplerSimple.NODE_CLASS_MAPPINGS,
    **forsenprompt.NODE_CLASS_MAPPINGS,
    **ming_nodes.NODE_CLASS_MAPPINGS,
    **mingDiffLoad.NODE_CLASS_MAPPINGS,
    **mingSTRINGtimer.NODE_CLASS_MAPPINGS,
    **pilgramfilter.NODE_CLASS_MAPPINGS,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **forsen_datetime.NODE_DISPLAY_NAME_MAPPINGS,
    **forsen_count.NODE_DISPLAY_NAME_MAPPINGS,
    **preset_loader.NODE_DISPLAY_NAME_MAPPINGS,
    **forsenKsamplerSelect.NODE_DISPLAY_NAME_MAPPINGS,
    **ForsenKsamplerSimple.NODE_DISPLAY_NAME_MAPPINGS,
    **forsenprompt.NODE_DISPLAY_NAME_MAPPINGS,
    **ming_nodes.NODE_DISPLAY_NAME_MAPPINGS,
    **mingDiffLoad.NODE_DISPLAY_NAME_MAPPINGS,
    **mingSTRINGtimer.NODE_DISPLAY_NAME_MAPPINGS,
    **pilgramfilter.NODE_DISPLAY_NAME_MAPPINGS,
}

WEB_DIRECTORY = "./web/js"

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]
