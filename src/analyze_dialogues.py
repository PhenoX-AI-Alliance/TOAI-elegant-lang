import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)

    speaker_counts = Counter()
    word_counts = defaultdict(Counter)

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
                    
                    # Simple whitespace tokenization as proxy for roots/words
                    tokens = text.split()
                    for token in tokens:
                        cleaned = token.strip(".,!?()[]{}\"\':;").lower()
                        if cleaned:
                            word_counts[speaker][cleaned] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {{line_num}}: {{jde}}", file=sys.stderr)
        
        result = {
            "total_speakers": len(speaker_counts),
            "speaker_utterance_counts": dict(speaker_counts),
            "speaker_top_words": {
                sp: dict(cnt.most_common(10)) for sp, cnt in word_counts.items()
            }
        }
        
        output_dir = "/home/phenox/gemini-sandbox/TOAI_Generated"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "dialogue_analysis_report.json")
        
        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print(f"Successfully analyzed dialogues. Report saved to {{output_path}}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
