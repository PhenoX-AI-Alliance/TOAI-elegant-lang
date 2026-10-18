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
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                speaker = data.get("speaker", "Unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
                for w in words:
                    word_counts[w] += 1
                    
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(20))
        }
        
        output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, "dialogue_analysis.json")
        
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(result, out, ensure_ascii=False, indent=2)
            
        print("Successfully analyzed dialogues and saved result to", output_file)
        
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
