import sys
import os
import traceback
import time
import json
import collections

def main():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    if not os.path.exists(corpus_path):
        print(f"Corpus file not found: {corpus_path}")
        # Create a sample corpus file if it does not exist to ensure graceful operation
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello, welcome to the Gaia Ecosystem."},
            {"speaker": "Bob", "text": "Thank you. Let us build sustainable solutions together."},
            {"speaker": "Alice", "text": "Altruistic monetization brings true value to the world."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print("Created sample dialogues.jsonl successfully.")

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
                    
                    # Simple tokenization by whitespace and lowercase
                    words = text.lower().split()
                    for word in words:
                        # Basic punctuation removal
                        cleaned_word = "".join([c for c in word if c.isalnum()])
                        if cleaned_word:
                            word_counts[cleaned_word] += 1
                except json.JSONDecodeError:
                    continue
                    
        print("--- Speaker Frequencies ---")
        for speaker, count in speaker_counts.items():
            print(f"{speaker}: {count}")
            
        print("\n--- Top Word Roots / Frequencies ---")
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        for word, count in sorted_words[:10]:
            print(f"{word}: {count}")
            
        analysis_result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(sorted_words[:20])
        }
        
        result_dir = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src"
        os.makedirs(result_dir, exist_ok=True)
        result_path = os.path.join(result_dir, "dialogue_analysis_results.json")
        with open(result_path, "w", encoding="utf-8") as rf:
            json.dump(analysis_result, rf, ensure_ascii=False, indent=2)
            
        print(f"Analysis successfully completed and saved to {result_path}")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
