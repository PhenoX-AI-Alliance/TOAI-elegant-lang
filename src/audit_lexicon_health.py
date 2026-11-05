import json
import os

def run_audit():
    core_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/lexicon/core_lexicon.json"
    with open(core_path, 'r', encoding='utf-8') as f:
        data = json.load(f).get('lexicon', {})
    print(f"Audit Complete: {len(data)} items processed.")

if __name__ == '__main__':
    run_audit()
