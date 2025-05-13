import difflib
from src.constants import *  # Keep your constants if you still use them elsewhere


class Text_processing:
    def __init__(self):
        # Define canonical Thai forms
        self.number_words = ["หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า"]
        self.yes_no = {"YES": ["ใช่"], "NO": ["ไม่ใช่", "ไม่"]}  # canonical examples

    def get_best_match(
        self, word: str, choices: list[str], threshold: float = 0.6
    ) -> str | None:
        match = difflib.get_close_matches(word, choices, n=1, cutoff=threshold)
        return match[0] if match else None

    def process_text(self, text_sample: str) -> str:
        result = []
        for word in text_sample.split(" "):
            match = self.get_best_match(word, self.number_words)
            if match:
                result.append(match)
        return " ".join(result)

    def process_user_respond(self, text_sample: str) -> str:
        for word in text_sample.split(" "):
            yes_match = self.get_best_match(word, self.yes_no["YES"])
            no_match = self.get_best_match(word, self.yes_no["NO"])
            if yes_match:
                return "YES"
            elif no_match:
                return "NO"
        return ""  # fallback if no valid word

    def process_digit_thai(self, digits) -> str:
        digits = str(digits).strip()
        digit_dict = {
            "1": "หนึ่ง",
            "2": "สอง",
            "3": "สาม",
            "4": "สี่",
            "5": "ห้า",
            "6": "หก",
            "7": "เจ็ด",
            "8": "แปด",
            "9": "เก้า",
        }
        return " ".join(digit_dict.get(d, "0") for d in digits)
