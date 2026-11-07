import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_root_counts = collections.defaultdict(int)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                speaker_counts[speaker] += 1
                
                text = data.get("text", "")
                words = text.split()
                for word in words:
                    root = word.lower().strip(".,!?\"'")
                    if root:
                        word_root_counts[root] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line: {e}")
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_word_roots": dict(word_root_counts.most_common(50))
    }
    
    output_json_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_result.json"
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print(f"Analysis successfully completed and saved to {output_json_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
