import sys
import os
import traceback
import time
import json
import collections

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
    os.makedirs(output_dir, exist_ok=True)
    output_report = os.path.join(output_dir, "dialogue_analysis_report.json")

    if not os.path.exists(corpus_path):
        print(f"Warning: {corpus_path} not found. Creating a dummy corpus for demonstration.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello, Gaia ecosystem! Let us build a sustainable future."},
            {"speaker": "Bob", "text": "Agreed. Altruistic capitalism brings true value to society."},
            {"speaker": "Alice", "text": "Wonderful. Warmth and efficiency can coexist."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    speaker_counts = collections.defaultdict(int)
    word_freq = collections.defaultdict(int)

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    speaker = record.get("speaker", "Unknown")
                    text = record.get("text", "")
                    speaker_counts[speaker] += 1
                    
                    words = text.lower().split()
                    for word in words:
                        cleaned = "".join(ch for ch in word if ch.isalnum())
                        if cleaned:
                            word_freq[cleaned] += 1
                except json.JSONDecodeError as jde:
                    print(f"JSON decode error at line {line_num}: {jde}")
    except Exception as e:
        print(f"Error reading corpus file: {e}")
        traceback.print_exc()
        sys.exit(1)

    report = {
        "speaker_utterance_counts": dict(speaker_counts),
        "top_word_frequencies": dict(sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:50]),
        "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(output_report, "w", encoding="utf-8") as out:
            json.dump(report, out, ensure_ascii=False, indent=4)
        print(f"Successfully analyzed corpus. Report saved to {output_report}")
    except Exception as e:
        print(f"Error writing analysis report: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
