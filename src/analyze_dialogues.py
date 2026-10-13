import sys
import os
import json
import collections

def analyze():
    input_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found at {input_path}")
        
    speaker_counts = collections.Counter()
    word_counts = collections.Counter()
    
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            speaker = data.get("speaker", "unknown")
            text = data.get("text", "")
            speaker_counts[speaker] += 1
            words = text.lower().split()
            for w in words:
                cleaned = "".join(ch for ch in w if ch.isalnum())
                if cleaned:
                    word_counts[cleaned] += 1
                    
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": word_counts.most_common(10)
    }
    
    output_result_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_result.json"
    with open(output_result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Analysis completed successfully. Result saved to {output_result_path}")

if __name__ == "__main__":
    analyze()
