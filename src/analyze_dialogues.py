import sys
import os
import traceback
import time
import json
import collections
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_freq = collections.defaultdict(int)
    
    print(f"Reading corpus from {{corpus_path}}...", flush=True)
    
    try:
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
                    
                    words = re.findall(r"\w+", text.lower())
                    for w in words:
                        if len(w) > 2:
                            word_freq[w] += 1
                except json.JSONDecodeError:
                    print(f"Warning: JSON decode error at line {{line_num}}", file=sys.stderr)
                    
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:50])
        }
        
        output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
        with open(output_result_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print(f"Analysis successfully completed and saved to {{output_result_path}}", flush=True)
        print("Speaker counts:", speaker_counts)
        
    except Exception as e:
        print(f"Error during analysis: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        print(f"Fatal error: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
