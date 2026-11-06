import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = defaultdict(Counter)
    
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
                for word in words:
                    cleaned_word = word.strip(".,!?()[]{}":;").lower()
                    if cleaned_word:
                        word_counts[speaker][cleaned_word] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "speaker_word_frequencies": {sp: dict(cnt.most_common(50)) for sp, cnt in word_counts.items()}
    }
    
    output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "dialogue_analysis_report.json")
    
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print(f"Analysis successfully completed. Report saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
