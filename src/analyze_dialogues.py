import sys
import os
import traceback
import time
import json
import collections
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print("Corpus file not found: " + corpus_path)
        sys.exit(1)

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    speaker = data.get("speaker", "unknown")
                    speaker_counts[speaker] += 1

                    text = data.get("text", "")
                    words = re.findall(r"\b\w+\b", text.lower())
                    for word in words:
                        word_counts[word] += 1
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print("Error reading corpus: " + str(e))
        traceback.print_exc()
        sys.exit(1)

    result = {
        "speaker_counts": dict(speaker_counts),
        "top_words": dict(word_counts.most_common(50))
    }

    output_result_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_result.json"
    os.makedirs(os.path.dirname(output_result_path), exist_ok=True)
    
    with open(output_result_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)

    print("Analysis complete. Result saved to " + output_result_path)

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        print("Fatal error: " + str(e))
        traceback.print_exc()
        sys.exit(1)
