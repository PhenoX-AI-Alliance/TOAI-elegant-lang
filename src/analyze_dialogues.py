import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_report = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_report.json"
    
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}. Creating a dummy corpus for robust execution.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Gaia", "text": "Welcome to the Earth of Life ecosystem and altruistic monetization."},
            {"speaker": "Human", "text": "Let us build robust systems and collaborate for a better future."},
            {"speaker": "Gaia", "text": "Warmth and high precision guide our path forward."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
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
                    cleaned = "".join(ch for ch in w if ch.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1
        
        report = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]),
            "timestamp": time.time()
        }
        
        with open(output_report, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"Analysis successfully completed. Report saved to {output_report}")
        
    except Exception as e:
        print(f"Error during dialogue analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
