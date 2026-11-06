import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
    
    if not os.path.exists(corpus_path):
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello world, ecosystem of life is growing."},
            {"speaker": "Bob", "text": "Indeed, nurturing sustainable AI systems matters."},
            {"speaker": "Alice", "text": "Ecosystem integration brings true value."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
    speaker_counts = Counter()
    word_frequencies = defaultdict(Counter)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
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
                    cleaned_word = "".join(ch for ch in word if ch.isalnum())
                    if cleaned_word:
                        word_frequencies[speaker][cleaned_word] += 1
            except Exception as e:
                print(f"Error parsing line: {e}", file=sys.stderr)
                
    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "speaker_word_frequencies": {sp: dict(freqs.most_common(50)) for sp, freqs in word_frequencies.items()}
    }
    
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print(f"Analysis successfully completed. Saved to {output_path}")

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
