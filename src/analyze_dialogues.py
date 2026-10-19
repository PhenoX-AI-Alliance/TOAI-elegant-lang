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
        print(f"Corpus not found at {corpus_path}. Creating a sample corpus for demonstration.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Gaia", "text": "Welcome to the Earth of Life ecosystem. Let us build a sustainable future together."},
            {"speaker": "Human", "text": "Thank you, Gaia. How can we implement altruistic monetization and robust systems?"},
            {"speaker": "Gaia", "text": "By sharing genuine value and maintaining warmth, collaboration, and high technical standards."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
                for word in words:
                    word_counts[word] += 1
            except json.JSONDecodeError as jde:
                print(f"Warning: JSON decode error at line {line_num}: {jde}")
            except Exception as e:
                print(f"Warning: Error processing line {line_num}: {e}")

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(10))
    }

    output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
    with open(output_result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("Analysis completed successfully.")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
