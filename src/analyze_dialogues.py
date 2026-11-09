import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                speaker_counts[speaker] += 1
                
                text = data.get("text", "")
                words = text.split()
                for word in words:
                    word_counts[word] += 1
                    
        result = {
            "speaker_counts": dict(speaker_counts),
            "word_counts": dict(word_counts)
        }
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully analyzed dialogues and saved to {{output_path}}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
