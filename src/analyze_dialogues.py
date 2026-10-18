import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
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
                    
                    words = re.findall(r'[a-zA-Z぀-ヿ一-龯]+', text)
                    for word in words:
                        if len(word) > 1:
                            word_counts[word] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {line_num}: {jde}")
                    continue
                    
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(50) if hasattr(word_counts, "most_common") else sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50])
        }
        
        output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
        with open(output_result_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print(f"Analysis successfully completed. Results saved to {output_result_path}")
        
    except Exception as e:
        print(f"Error during dialogue analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
