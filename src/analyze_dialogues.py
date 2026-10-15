import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_result.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
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
                    cleaned_w = "".join(ch for ch in w if ch.isalnum())
                    if cleaned_w:
                        word_counts[cleaned_w] += 1
                        
        result = {
            "speaker_counts": dict(speaker_counts),
            "word_frequencies": dict(word_counts.most_common(50)),
            "analyzed_at": time.time()
        }
        
        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print(f"Analysis successfully completed. Result saved to {output_path}")
        
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
