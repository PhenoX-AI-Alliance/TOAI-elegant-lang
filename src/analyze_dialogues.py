import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
    
    if not os.path.exists(corpus_path):
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello world, ecosystem of life."},
            {"speaker": "Bob", "text": "Welcome to the Gaia ecosystem and alturism."},
            {"speaker": "Alice", "text": "Let us build robust systems for sustainable growth."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
    speaker_counts = Counter()
    word_counts = defaultdict(Counter)
    
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
                    cleaned_word = "".join([c for c in word if c.isalnum()])
                    if cleaned_word:
                        word_counts[speaker][cleaned_word] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_utterances": dict(speaker_counts),
        "speaker_vocabulary": {sp: dict(cnt.most_common(10)) for sp, cnt in word_counts.items()}
    }
    
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print(f"Analysis complete. Results saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
