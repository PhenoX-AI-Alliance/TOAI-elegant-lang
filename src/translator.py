import sys
import os
import json

class ElegantTranslator:
    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.translation_map = self._load_map()

    def _load_map(self):
        if not os.path.exists(self.map_file_path):
            return {}
        with open(self.map_file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def decode(self, text):
        decoded_text = text
        # 長いキーから順に置換することで部分一致の誤爆を防ぐ
        sorted_keys = sorted(self.translation_map.keys(), key=len, reverse=True)
        for key in sorted_keys:
            value = self.translation_map[key]
            decoded_text = decoded_text.replace(key, f"[{value}]")
        return decoded_text

    def encode(self, text):
        encoded_text = text
        # 逆引き辞書の作成
        inverse_map = {v: k for k, v in self.translation_map.items()}
        sorted_values = sorted(inverse_map.keys(), key=len, reverse=True)
        for value in sorted_values:
            key = inverse_map[value]
            encoded_text = encoded_text.replace(f"[{value}]", key)
            encoded_text = encoded_text.replace(value, key)
        return encoded_text

if __name__ == "__main__":
    map_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "translation_map.json"))
    translator = ElegantTranslator(map_path)
    sample = "~* から始まり -> へ至り =* を生む"
    print("Original:", sample)
    print("Decoded:", translator.decode(sample))
