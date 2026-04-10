import os
import glob


class ForsenCount:
    """
    Custom node to count images in a folder based on pattern.
    Outputs the total image count.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory_path": ("STRING", {
                    "default": "",
                    "multiline": False
                }),
                "pattern": ("STRING", {
                    "default": "*",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("image_count",)
    FUNCTION = "count_images"
    CATEGORY = "ming/main"

    def count_images(self, directory_path, pattern="*"):
        # allowed img exntesions
        ALLOWED_EXT = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')

        # Check if directory exists
        if not os.path.exists(directory_path):
            print(f"Error: Directory '{directory_path}' does not exist")
            return (0,)

        # Use glob to find images matching the pattern with recursive=True
        try:
            image_count = 0
            for file_path in glob.glob(os.path.join(glob.escape(directory_path), pattern), recursive=True):
                # Check if file ends with allowed extension
                if file_path.lower().endswith(ALLOWED_EXT):
                    image_count += 1

            print(f"Found {image_count} images in '{directory_path}' with pattern '{pattern}'")
            return (image_count,)

        except Exception as e:
            print(f"Error counting images: {e}")
            return (0,)


NODE_CLASS_MAPPINGS = {
    "ForsenCount": ForsenCount
}

# UI display name
NODE_DISPLAY_NAME_MAPPINGS = {
    "ForsenCount": "Forsen Count"
}
