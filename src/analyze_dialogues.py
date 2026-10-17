import sys
import os
import traceback
import time
import json
import collections

def main():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_report.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_root_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    speaker = record.get("speaker", "unknown")
                    text = record.get("text", "")
                    
                    speaker_counts[speaker] += 1
                    
                    words = text.split()
                    for word in words:
                        root = word.lower().strip(".,!?\"'()[]{}<>:;")
                        if root:
                            word_root_counts[root] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {{line_num}}: {{jde}}", file=sys.stderr)
                except Exception as ex:
                    print(f"Warning: Error processing line {{line_num}}: {{ex}}", file=sys.stderr)
                    
        report = {
            "timestamp": time.time(),
            "speaker_counts": dict(speaker_counts),
            "top_word_roots": dict(sorted(word_root_counts.items(), key=lambda item: item[1], reverse=True)[:50])
        }
        
        os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
        with open(output_report_path, "w", encoding="utf-8") as out:
            json.dump(report, out, ensure_ascii=False, indent=2)
            
        print(f"Analysis successfully completed. Report saved to {{output_report_path}}")
        
    except Exception as e:
        print(f"Critical error during analysis: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
