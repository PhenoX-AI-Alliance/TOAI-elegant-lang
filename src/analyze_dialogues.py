import sys
import os
import traceback
import time
import json
from collections import Counter, defaultdict

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    if not os.path.exists(corpus_path):
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello world, ecosystem of life."},
            {"speaker": "Bob", "text": "Greetings, let us build robust systems."},
            {"speaker": "Alice", "text": "Altruistic monetization brings true value."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
    speaker_counts = Counter()
    word_frequencies = defaultdict(Counter)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                text = data.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for word in words:
                    cleaned_word = "".join(ch for ch in word if ch.isalnum())
                    if cleaned_word:
                        word_frequencies[speaker][cleaned_word] += 1
                        
        result = {
            "speaker_utterance_counts": dict(speaker_counts),
            "speaker_word_frequencies": {sp: dict(counts) for sp, counts in word_frequencies.items()}
        }
        
        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, indent=2, ensure_ascii=False)
            
        print("Analysis completed successfully. Results saved to:", output_path)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
