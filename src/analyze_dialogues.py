import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_report.json"

    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}. Creating a dummy corpus for robust execution.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello Gaia ecosystem, let us build wonderful systems."},
            {"speaker": "Bob", "text": "Greetings Alice. Altruistic monetization brings true value."},
            {"speaker": "Alice", "text": "Indeed, robust code and warm interactions create harmony."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    speaker_counts = Counter()
    word_counts = Counter()

    try:
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
                    for word in words:
                        cleaned = "".join([c for c in word if c.isalnum()])
                        if cleaned:
                            word_counts[cleaned] += 1
                except json.JSONDecodeError:
                    continue

        report = {
            "timestamp": time.time(),
            "speaker_counts": dict(speaker_counts),
            "top_words": word_counts.most_common(20)
        }

        os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
        with open(output_report_path, "w", encoding="utf-8") as out_f:
            json.dump(report, out_f, ensure_ascii=False, indent=2)

        print("Dialogue analysis completed successfully.")
        print(f"Report saved to {output_report_path}")

    except Exception as e:
        print(f"Error during dialogue analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
