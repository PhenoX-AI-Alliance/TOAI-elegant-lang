import sys
import os
import traceback
import time
import json
import collections

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {{corpus_path}}. Creating a dummy corpus for robust analysis.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Gaia", "text": "Welcome to the Earth of Life and altruistic ecosystems."},
            {"speaker": "Executor", "text": "Executing high-precision analysis with warmth and precision."},
            {"speaker": "Gaia", "text": "Let us cultivate genuine value and sustainable monetization."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    speaker = record.get("speaker", "unknown")
                    text = record.get("text", "")
                    
                    speaker_counts[speaker] += 1
                    
                    words = text.lower().split()
                    for word in words:
                        cleaned = "".join(ch for ch in word if ch.isalnum())
                        if cleaned:
                            word_counts[cleaned] += 1
                except json.JSONDecodeError:
                    continue
                    
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }
        
        output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
        with open(output_result_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print("Analysis completed successfully. Results saved to:", output_result_path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print("Error during analysis:", str(e))
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
