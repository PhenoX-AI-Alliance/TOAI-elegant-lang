import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print("Error: Corpus file not found.")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                speaker = data.get("speaker", "Unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for w in words:
                    cleaned_word = "".join(ch for ch in w if ch.isalnum())
                    if cleaned_word:
                        word_counts[cleaned_word] += 1
                        
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(10))
        }
        
        output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "analysis_result.json")
        
        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print("Analysis completed successfully. Results saved to:", out_path)
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
