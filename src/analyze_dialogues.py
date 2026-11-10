import sys
import os
import traceback
import time
import json
import collections

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}", file=sys.stderr)
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
                    root = word.strip(".,!?\"'()[]{}:;").lower()
                    if root:
                        word_root_counts[root] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "word_root_counts": dict(word_root_counts.most_common(100))
    }
    
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dialogue_analysis.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Analysis successfully written to {output_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
