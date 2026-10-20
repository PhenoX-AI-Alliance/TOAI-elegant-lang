import sys
import os
import traceback
import time
import json
from collections import defaultdict, Counter

def main():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_report = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_report.json"

    speaker_counts = Counter()
    word_root_counts = Counter()

    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
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
                    
                    # Simple tokenization / root extraction simulation for elegant lang
                    tokens = text.split()
                    for token in tokens:
                        cleaned = ''.join(c for c in token if c.isalnum()).lower()
                        if len(cleaned) > 2:
                            word_root_counts[cleaned] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {line_num}: {jde}")

        report = {
            "total_speakers": len(speaker_counts),
            "speaker_utterance_counts": dict(speaker_counts.most_common()),
            "top_word_roots": dict(word_root_counts.most_common(50)),
            "analyzed_at": time.time()
        }

        with open(output_report, "w", encoding="utf-8") as out_f:
            json.dump(report, out_f, ensure_ascii=False, indent=2)

        print(f"Successfully analyzed dialogues. Report saved to {output_report}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
