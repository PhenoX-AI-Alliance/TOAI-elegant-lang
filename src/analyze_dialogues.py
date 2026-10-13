import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print("Error: Corpus file not found at " + corpus_path)
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                speaker = record.get("speaker", "Unknown")
                text = record.get("text", "")
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for w in words:
                    cleaned = "".join(ch for ch in w if ch.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1
            except Exception as e:
                print("Warning: Failed to parse line: " + str(e))
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(10))
    }
    
    output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "dialogue_analysis_result.json")
    
    with open(out_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print("Dialogue analysis successfully completed. Result saved to " + out_path)

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
