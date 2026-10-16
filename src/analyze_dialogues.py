import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = Counter()
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    speaker = record.get("speaker", "Unknown")
                    text = record.get("text", "")
                    
                    speaker_counts[speaker] += 1
                    
                    words = text.lower().split()
                    for word in words:
                        cleaned = "".join([c for c in word if c.isalnum()])
                        if cleaned:
                            word_counts[cleaned] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {line_num}: {jde}")
                    
        print("=== Speaker Turn Counts ===")
        for speaker, count in speaker_counts.items():
            print(f"{speaker}: {count}")
            
        print("\n=== Top Root Words / Frequencies ===")
        for word, count in word_counts.most_common(10):
            print(f"{word}: {count}")
            
        result_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
        os.makedirs(result_dir, exist_ok=True)
        result_path = os.path.join(result_dir, "dialogue_analysis_result.json")
        
        output_data = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(20)),
            "timestamp": time.time()
        }
        
        with open(result_path, "w", encoding="utf-8") as out:
            json.dump(output_data, out, ensure_ascii=False, indent=2)
            
        print(f"\nAnalysis successfully completed and saved to {result_path}")
        
    except Exception as e:
        print(f"Unexpected error during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
