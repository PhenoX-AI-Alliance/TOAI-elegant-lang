import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    if not os.path.exists(corpus_path):
        print(f"Corpus not found at {corpus_path}. Creating a dummy corpus for demonstration.")
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello world of the Earth of Life."},
            {"speaker": "Bob", "text": "Greetings, let us build sustainable systems together."},
            {"speaker": "Alice", "text": "Altruistic monetization brings true value."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
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
                    cleaned_word = "".join([c for c in word if c.isalnum()])
                    if cleaned_word:
                        word_counts[cleaned_word] += 1
                        
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(10))
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print("Analysis completed successfully. Results saved to:", output_path)
    except Exception as e:
        print(f"Error during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
