import sys
import os
import traceback
import time
import json
import collections
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        # Create a dummy corpus for robust execution if missing
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Gaia", "text": "Hello world, welcome to the Earth of Life ecosystem."},
            {"speaker": "Human", "text": "Thank you, Gaia. Let us build a sustainable future together."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print("Created sample corpus for initialization.")

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(lambda: collections.defaultdict(int))

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
                    
                    # Simple root word extraction (lowercased alphanumeric tokens)
                    words = re.findall(r'\b[a-z0-9]{3,}\b', text.lower())
                    for word in words:
                        word_counts[speaker][word] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {line_num}: {jde}")
                except Exception as e:
                    print(f"Warning: Error processing line {line_num}: {e}")

        result = {
            "speaker_utterance_counts": dict(speaker_counts),
            "speaker_word_frequencies": {sp: dict(cnt.most_common(10)) for sp, cnt in word_counts.items()}
        }

        output_json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_results.json"
        with open(output_json_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, indent=2, ensure_ascii=False)

        print(f"Successfully analyzed dialogues. Results saved to {output_json_path}")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Critical error during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
