import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    result_file = os.path.join(output_dir, "dialogue_analysis.json")

    speaker_counts = collections.defaultdict(int)
    word_root_counts = collections.defaultdict(int)

    if not os.path.exists(corpus_path):
        print(f"Warning: {corpus_path} not found. Creating a sample corpus for demonstration.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello world, computation is life."},
            {"speaker": "Bob", "text": "Computing values brings joy and sustainability."},
            {"speaker": "Alice", "text": "Let us compute kindness and altruism."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    speaker = record.get("speaker", "unknown")
                    text = record.get("text", "")
                    
                    speaker_counts[speaker] += 1
                    
                    words = text.lower().split()
                    for word in words:
                        cleaned = "".join([c for c in word if c.isalnum()])
                        if cleaned:
                            root = cleaned[:4]
                            word_root_counts[root] += 1
                except json.JSONDecodeError as jde:
                    print(f"JSON decode error at line {line_num}: {jde}")
                    continue

        analysis_result = {
            "speaker_counts": dict(speaker_counts),
            "word_root_counts": dict(word_root_counts),
            "analyzed_at": time.time()
        }

        with open(result_file, "w", encoding="utf-8") as rf:
            json.dump(analysis_result, rf, ensure_ascii=False, indent=2)

        print(f"Successfully analyzed dialogues. Results saved to {result_file}")

    except Exception as e:
        print(f"Error during dialogue analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
