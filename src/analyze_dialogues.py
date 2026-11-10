import sys
import os
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = Counter()
    word_counts = defaultdict(Counter)
    
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            speaker = data.get("speaker", "Unknown")
            text = data.get("text", "")
            
            speaker_counts[speaker] += 1
            
            words = text.lower().split()
            for word in words:
                cleaned_word = "".join(c for c in word if c.isalnum())
                if cleaned_word:
                    word_counts[speaker][cleaned_word] += 1
                    
    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "speaker_vocabulary": {sp: dict(wc.most_common(10)) for sp, wc in word_counts.items()}
    }
    
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_result.json"
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(result, out_f, ensure_ascii=False, indent=2)
        
    print("Analysis completed successfully. Result saved to", output_path)

if __name__ == "__main__":
    try:
        analyze()
    except Exception as e:
        print("Error during analysis:", str(e))
        sys.exit(1)
