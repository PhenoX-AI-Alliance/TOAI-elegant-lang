import sys
import os
import traceback
import time
import json
import collections

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_json = os.path.join(output_dir, "dialogue_analysis.json")

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    if not os.path.exists(corpus_path):
        print(f"Warning: Corpus not found at {corpus_path}. Generating sample data for demonstration.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Gaia", "text": "Hello world, let us build a sustainable and warm ecosystem together."},
            {"speaker": "Human", "text": "I agree, altruistic monetization and technology will save our future."},
            {"speaker": "Gaia", "text": "Wonderful! Let us write clean python code and verify it."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

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
                    
                    words = text.lower().split()
                    for word in words:
                        cleaned = "".join(ch for ch in word if ch.isalnum())
                        if cleaned:
                            word_counts[cleaned] += 1
                except json.JSONDecodeError as jde:
                    print(f"JSON decode error at line {line_num}: {jde}")
                except Exception as ex:
                    print(f"Error processing line {line_num}: {ex}")

        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(50)),
            "analyzed_at": time.time()
        }

        with open(output_json, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)

        print(f"Successfully analyzed dialogues. Results saved to {output_json}")

    except Exception as e:
        print(f"Failed during corpus analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
