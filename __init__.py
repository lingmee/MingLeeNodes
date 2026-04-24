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

def display_minglee_banner(node_mappings):
    clr_border = "\033[38;2;203;166;247m"   # mauve
    clr_title = "\033[38;2;245;224;220m"    # rosewater
    clr_label = "\033[38;2;180;190;254m"    # lavender
    clr_ok = "\033[38;2;166;227;161m"       # green
    clr_count = "\033[38;2;250;179;135m"    # peach
    clr_subtle = "\033[38;2;166;173;200m"   # subtext
    clr_reset = "\033[0m"
    clr_bold = "\033[1m"

    node_count = len(node_mappings)
    bar = f"{clr_border}{'=' * 58}{clr_reset}"

    print(bar)
    print(f"{clr_bold}{clr_title}MingLee Nodes{clr_reset}")
    print(f"{clr_border}-{clr_reset} {clr_label}Status:{clr_reset} {clr_ok}Loaded successfully{clr_reset}")
    print(f"{clr_border}-{clr_reset} {clr_label}Nodes:{clr_reset}  {clr_count}{node_count}{clr_reset} {clr_subtle}total{clr_reset}")
    print(f"{clr_border}-{clr_reset} {clr_subtle}\"better piss in the sink, than sink in the piss\"{clr_reset}")
    print(bar)

display_minglee_banner(NODE_CLASS_MAPPINGS)