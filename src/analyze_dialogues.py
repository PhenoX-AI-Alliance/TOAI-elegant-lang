import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def main():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_report.json"
    
    speaker_counts = Counter()
    word_counts = Counter()
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)
        
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
                    
                    words = text.split()
                    for word in words:
                        clean_word = word.strip(".,!?()[]{}":;''").lower()
                        if clean_word:
                            word_counts[clean_word] += 1
                            
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {{line_num}}: {{jde}}", file=sys.stderr)
                    
        report = {
            "speaker_utterance_counts": dict(speaker_counts),
            "top_words": word_counts.most_common(50),
            "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
        with open(output_report_path, "w", encoding="utf-8") as out_f:
            json.dump(report, out_f, ensure_ascii=False, indent=2)
            
        print(f"Analysis complete. Report saved to {{output_report_path}}")
        
    except Exception as e:
        print(f"Error during analysis: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
