import os

BASE_DIR = r"D:\Prompts\iTools"


def get_prompt_files():
    if not os.path.isdir(BASE_DIR):
        return ["<folder not found>"]

    files = [
        f for f in os.listdir(BASE_DIR)
        if f.lower().endswith(".txt")
    ]

    return files if files else ["<no txt files>"]


class FileHandler:
    def __init__(self, filename):
        self.filename = filename
        self.lines = None

    def read_line(self, line_index):
        """Read a specific line from the file by its index (0-based)."""
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line for line in lines if line.strip()]  # Ignore empty lines
            if self.lines is None:
                self.lines = lines
            if 0 <= line_index < len(lines):
                return lines[line_index].strip()
            else:
                raise IndexError("Line index out of range.")

    def len_lines(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line for line in lines if line.strip()]  # Ignore empty lines
        return len(lines)

    def append_line(self, line):
        """Append a line to the end of the file."""
        with open(self.filename, 'a') as file:
            file.write(line + '\n')

    def load_lines(self):
        """Load all lines from the file into a list."""
        with open(self.filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]

    def escape_quotes(self, text):
        return text.replace('"', '\\"').replace("'", "\\'")

    def unescape_quotes(self, text):
        return text.replace('\\"', '"').replace("\\'", "'")


class ForsenPromptLoader:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt_file": (get_prompt_files(),),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFF}),
            }
        }

    CATEGORY = "Forsen/prompt"
    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("prompt", "count")
    FUNCTION = "load_file"

    DESCRIPTION = "Loads a prompt line from a TXT file in D:\\Prompts\\iTools"

    def load_file(self, prompt_file, seed, fallback="Yes"):
        file_path = os.path.join(BASE_DIR, prompt_file)

        prompt = ""
        count = 0

        if os.path.exists(file_path):
            fh = FileHandler(file_path)
            try:
                count = fh.len_lines()
                line = fh.read_line(seed)
                prompt = fh.unescape_quotes(line)
            except IndexError:
                if fallback == "Yes" and count > 0:
                    seed %= count
                    line = fh.read_line(seed)
                    prompt = fh.unescape_quotes(line)
        else:
            prompt = f"File not found: {file_path}"

        return prompt, count


NODE_CLASS_MAPPINGS = {
    "ForsPromptLoader": ForsenPromptLoader,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ForsenPromptLoader": "ForsenPromptLoader",
}
