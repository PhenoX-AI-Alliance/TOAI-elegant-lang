import sys
import os
import traceback
import time
import json
import collections
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_frequencies = collections.defaultdict(int)
    
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
                
                words = re.findall(r"\w+", text.lower())
                for word in words:
                    if len(word) > 2:
                        word_frequencies[word] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:50]),
        "timestamp": time.time()
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully analyzed corpus. Results saved to {{output_path}}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
