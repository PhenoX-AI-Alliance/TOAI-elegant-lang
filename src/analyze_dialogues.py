import sys
import os
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: {corpus_path} not found.", file=sys.stderr)
        sys.exit(1)

    speaker_counts = collections.Counter()
    word_counts = collections.Counter()

    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                text = data.get("text", "")
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for w in words:
                    cleaned = "".join(c for c in w if c.isalnum())
                    if cleaned:
                        word_counts[cleaned] += 1
            except json.JSONDecodeError:
                continue

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": word_counts.most_common(10)
    }

    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)

    print(f"Successfully analyzed dialogues. Results saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)
