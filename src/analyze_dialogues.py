import sys
import os
import traceback
import time
import json
import collections
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = re.findall(r"\b\w+\b", text.lower())
                for word in words:
                    if len(word) > 2:
                        word_counts[word] += 1
            except json.JSONDecodeError as e:
                print(f"Warning: JSON decode error at line {line_num}: {e}")
            except Exception as e:
                print(f"Warning: Error processing line {line_num}: {e}")
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50]),
        "analyzed_at": time.time()
    }
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully analyzed corpus. Results saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
