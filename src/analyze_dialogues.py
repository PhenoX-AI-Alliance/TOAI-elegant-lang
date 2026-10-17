import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}", file=sys.stderr)
        sys.exit(1)

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                speaker = record.get("speaker", "unknown")
                text = record.get("text", "")
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for w in words:
                    cleaned_w = "".join([c for c in w if c.isalnum()])
                    if cleaned_w:
                        word_counts[cleaned_w] += 1
            except Exception as e:
                print(f"Warning: Parse error: {e}", file=sys.stderr)

    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "top_word_frequencies": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]),
        "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    output_json_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    with open(output_json_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
    print(f"Analysis completed successfully. Saved to {output_json_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
