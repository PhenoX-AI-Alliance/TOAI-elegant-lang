import sys
import os
import json
from collections import Counter

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)

    speaker_counts = Counter()
    word_counts = Counter()

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                speaker = data.get('speaker', 'unknown')
                text = data.get('text', '')
                speaker_counts[speaker] += 1
                
                words = text.split()
                for w in words:
                    word_counts[w.lower()] += 1
            except json.JSONDecodeError:
                continue

    result = {
        "speaker_counts": speaker_counts.most_common(),
        "top_words": word_counts.most_common(50)
    }

    output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
    with open(output_result_path, 'w', encoding='utf-8') as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)

    print(f"Analysis completed successfully. Results saved to {output_result_path}")

if __name__ == "__main__":
    analyze_corpus()
