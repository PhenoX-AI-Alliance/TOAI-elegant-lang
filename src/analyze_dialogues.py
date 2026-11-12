import sys
import os
import traceback
import json
from collections import Counter, defaultdict
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = Counter()
    word_frequencies = Counter()
    
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
                
                words = re.findall(r'\b\w+\b', text.lower())
                for word in words:
                    if len(word) > 2:
                        word_frequencies[word] += 1
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse JSON at line {line_num}: {e}")
            except Exception as e:
                print(f"Warning: Unexpected error at line {line_num}: {e}")
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_frequencies.most_common(50))
    }
    
    output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
    with open(output_result_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print(f"Successfully analyzed dialogues. Results saved to {output_result_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
