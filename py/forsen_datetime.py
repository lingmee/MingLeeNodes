import datetime


class ForsenDate:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {}
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("date_string",)
    FUNCTION = "get_date"
    CATEGORY = "utils/date"

    def get_date(self):
        now = datetime.datetime.now()
        date_str = now.strftime("%d-%m-%y")
        return (date_str,)


NODE_CLASS_MAPPINGS = {
    "ForsenDate": ForsenDate
}

# UI display name
NODE_DISPLAY_NAME_MAPPINGS = {
    "ForsenDate": "Forsen Date"
}
