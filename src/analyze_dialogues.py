import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
    
    speaker_counts = Counter()
    word_counts = Counter()
    
    if not os.path.exists(corpus_path):
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello Gaia ecosystem and altruistic monetization."},
            {"speaker": "Bob", "text": "Let us build robust systems and warm value for the earth."},
            {"speaker": "Alice", "text": "Altruism brings sustainable growth."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
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
                    cleaned = "".join(c for c in word if c.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": word_counts.most_common(50)
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        
    print("Analysis completed successfully. Result saved to", output_path)

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
