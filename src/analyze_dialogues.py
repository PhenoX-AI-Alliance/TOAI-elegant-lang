import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze_dialogues():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    corpus_path = os.path.join(repo_dir, "corpus", "dialogues.jsonl")
    output_path = os.path.join(repo_dir, "src", "dialogue_analysis_result.json")
    
    speaker_counts = Counter()
    word_counts = defaultdict(Counter)
    
    if not os.path.exists(corpus_path):
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello, eco system and AI collaboration!"},
            {"speaker": "Bob", "text": "Let us build a sustainable future together."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
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
                for w in words:
                    cleaned = "".join(ch for ch in w if ch.isalnum())
                    if cleaned:
                        word_counts[speaker][cleaned] += 1
            except json.JSONDecodeError:
                continue
                
    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "speaker_word_frequencies": {sp: dict(wc.most_common(10)) for sp, wc in word_counts.items()}
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
    print("Analysis successfully completed and saved to:", output_path)

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
