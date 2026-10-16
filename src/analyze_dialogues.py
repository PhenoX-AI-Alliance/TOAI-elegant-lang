import sys
import os
import traceback
import time
import json
import collections
import re

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {{corpus_path}}. Creating a default sample corpus.")
        corpus_dir = os.path.dirname(corpus_path)
        os.makedirs(corpus_dir, exist_ok=True)
        
        sample_data = [
            {"speaker": "Gaia", "text": "Hello, welcome to the Earth of Life ecosystem. Let us build a sustainable future."},
            {"speaker": "Human", "text": "Thank you, Gaia. I want to learn how to analyze dialogues and build robust systems."},
            {"speaker": "Gaia", "text": "Dialogues are the bridge between human warmth and machine precision."}
        ]
        
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    speaker_counts = collections.Counter()
    word_counts = collections.Counter()
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
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
                    if len(word) > 2:
                        word_counts[word] += 1
            except Exception as e:
                print(f"Warning: Failed to parse line {{line_num}}: {{e}}")

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": word_counts.most_common(20)
    }
    
    output_report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_report.json"
    with open(output_report_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print("Analysis complete. Report saved to", output_report_path)
    print("Speaker Counts:", json.dumps(dict(speaker_counts), ensure_ascii=False))

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
