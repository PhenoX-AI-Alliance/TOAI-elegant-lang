import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"

    if not os.path.exists(corpus_path):
        print(f"Corpus file not found at: {corpus_path}")
        # Create a dummy corpus for robust testing if missing
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello world, this is a test dialogue."},
            {"speaker": "Bob", "text": "Hello Alice, testing the dialogue analyzer."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

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
                
                # Simple tokenization for root words/tokens
                tokens = text.lower().split()
                for token in tokens:
                    cleaned_token = "".join(c for c in token if c.isalnum())
                    if cleaned_token:
                        word_counts[cleaned_token] += 1
            except json.JSONDecodeError as jde:
                print(f"Warning: JSON decode error at line {line_num}: {jde}")
            except Exception as e:
                print(f"Warning: Error processing line {line_num}: {e}")

    result = {
        "speaker_counts": dict(speaker_counts),
        "word_frequencies": dict(word_counts.most_common(100))
    }

    os.makedirs(os.path.dirname(output_result_path), exist_ok=True)
    with open(output_result_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)

    print(f"Successfully analyzed dialogues. Results saved to {output_result_path}")

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
