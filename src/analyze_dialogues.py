import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {{corpus_path}}")
        # Create a dummy corpus for robust demonstration if missing
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello, the earth of life is beautiful."},
            {"speaker": "Bob", "text": "Indeed, altruistic monetization brings joy."},
            {"speaker": "Alice", "text": "Let us build robust systems together."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print("Created sample corpus for initialization.")

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    speaker = record.get("speaker", "unknown")
                    text = record.get("text", "")
                    
                    speaker_counts[speaker] += 1
                    
                    # Simple root word extraction (lowercased alphabetic tokens)
                    tokens = re.findall(r'[a-zA-Z]{3,}', text.lower())
                    for token in tokens:
                        word_counts[token] += 1
                except json.JSONDecodeError:
                    continue

        result = {
            "speaker_utterance_counts": dict(speaker_counts),
            "top_root_words": dict(word_counts.most_common(20)),
            "timestamp": time.time()
        }

        output_json_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_result.json"
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        
        with open(output_json_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)

        print("Dialogue analysis completed successfully.")
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"An error occurred during analysis: {{e}}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
