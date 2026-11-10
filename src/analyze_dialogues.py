import sys
import os
import json
import collections
import re

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "Unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = re.findall(r'\b\w+\b', text.lower())
                for word in words:
                    word_counts[word] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(10)) if hasattr(word_counts, "most_common") else dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    }
    
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_result.json"
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        
    print(f"Analysis complete. Results saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)
