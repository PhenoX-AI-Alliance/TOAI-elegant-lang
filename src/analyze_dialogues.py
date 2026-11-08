import sys
import os
import traceback
import json
import collections
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {{corpus_path}}", file=sys.stderr)
        sys.exit(1)

    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)

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
                    
                    words = re.findall(r'\w+', text.lower())
                    for word in words:
                        if len(word) > 2:
                            word_counts[word] += 1
                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON at line {{line_num}}", file=sys.stderr)

        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(50))
        }

        output_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "dialogue_analysis_result.json")

        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)

        print(f"Analysis complete. Results saved to {{output_path}}")

    except Exception as e:
        print(f"Error during analysis: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
