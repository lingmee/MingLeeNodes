import time
import execution


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")


def format_duration(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{minutes:02d}:{secs:02d}.{ms:03d}"


class GlobalTimer:
    start_time = None

    @classmethod
    def start(cls):
        cls.start_time = time.perf_counter()
        print(f"[Timer] Started")

    @classmethod
    def stop(cls):
        if cls.start_time is None:
            return 0
        elapsed = time.perf_counter() - cls.start_time
        cls.start_time = None
        return elapsed


class TimerInit:
    """
    DUMMY NODE - Place first. No inputs = runs immediately.
    Outputs signal to trigger TimerStart.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ("TIMER_SIGNAL",)
    RETURN_NAMES = ("signal",)
    FUNCTION = "execute"
    CATEGORY = "utils/timer"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Force execution every single time
        return float("nan")

    def execute(self):
        # Start timer here
        GlobalTimer.start()
        return (True,)


class TimerStart:
    """
    Place after TimerInit AND model loader.
    Waits for both: signal (always fresh) + model (possibly cached).
    Passes through the model unchanged.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "signal": ("TIMER_SIGNAL",),  # From TimerInit - always runs
                "model": ("MODEL",),          # From Checkpoint Loader - may be cached
            },
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "execute"
    CATEGORY = "utils/timer"

    def execute(self, signal, model):
        # Timer already started by TimerInit, just pass model through
        return (model,)


class TimerEnd:
    """
    Place at end of workflow. Outputs elapsed time string.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger": (any,),  # Connect final output here
            },
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("elapsed_time",)
    FUNCTION = "execute"
    OUTPUT_NODE = True
    CATEGORY = "utils/timer"

    def execute(self, trigger):
        elapsed = GlobalTimer.stop()
        time_str = format_duration(elapsed)
        print(f"[Timer] Total workflow time: {time_str}")
        return (time_str,)


NODE_CLASS_MAPPINGS = {
    "TimerInit": TimerInit,
    "TimerStart": TimerStart,
    "TimerEnd": TimerEnd,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TimerInit": "⏱️ Timer Init (First)",
    "TimerStart": "⏱️ Timer Start",
    "TimerEnd": "⏱️ Timer End",
}
