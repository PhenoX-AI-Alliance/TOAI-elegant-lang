import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.Counter()
    word_counts = collections.Counter()
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                speaker = data.get("speaker", "Unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for w in words:
                    cleaned = ''.join(c for c in w if c.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1
                        
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": word_counts.most_common(10)
        }
        
        output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
        with open(output_result_path, "w", encoding="utf-8") as out:
            json.dump(result, out, ensure_ascii=False, indent=2)
            
        print("Analysis completed successfully. Result saved to analysis_result.json")
    except Exception as e:
        print(f"Error during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
