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
        print("Error: Corpus path not found: " + corpus_path)
        sys.exit(1)

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

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
                    
                    # Simple tokenization for word frequency
                    words = re.findall(r'\w+', text.lower())
                    for word in words:
                        if len(word) > 2:
                            word_counts[word] += 1
                except json.JSONDecodeError:
                    print(f"Warning: JSON decode error at line {line_num}")
                    continue

        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(50))
        }

        output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "dialogue_analysis_result.json")
        
        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print("Analysis completed successfully. Saved to " + out_path)

    except Exception as e:
        print("Error during analysis: " + str(e))
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
