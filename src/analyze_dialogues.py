import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Corpus file not found: {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    speaker = data.get("speaker", "unknown")
                    text = data.get("text", "")
                    speaker_counts[speaker] += 1
                    words = text.split()
                    for w in words:
                        word_counts[w.lower()] += 1
                except json.JSONDecodeError:
                    continue
                    
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(50))
        }
        
        output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_result.json"
        with open(output_result_path, "w", encoding="utf-8") as out:
            json.dump(result, out, ensure_ascii=False, indent=2)
            
        print("Analysis completed successfully. Result saved to:", output_result_path)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()