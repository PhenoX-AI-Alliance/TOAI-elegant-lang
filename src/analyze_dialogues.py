import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    speaker_counts = Counter()
    word_frequencies = defaultdict(Counter)
    
    if not os.path.exists(corpus_path):
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello, eco system of life."},
            {"speaker": "Bob", "text": "Greetings, let us analyze the dialogues."}
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
                        word_frequencies[speaker][cleaned] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "word_frequencies": {sp: dict(counts.most_common(10)) for sp, counts in word_frequencies.items()}
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print("Dialogue analysis completed successfully.")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
