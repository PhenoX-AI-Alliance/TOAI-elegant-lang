import sys
import os
import traceback
import time
import json
import collections

def main():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/analysis_result.json"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                speaker = data.get("speaker", "unknown")
                speaker_counts[speaker] += 1
                
                text = data.get("text", "")
                words = text.split()
                for word in words:
                    cleaned_word = word.strip(".,!?\"'()[]{}<>").lower()
                    if cleaned_word:
                        word_counts[cleaned_word] += 1
                        
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:50])
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
            
        print(f"Analysis completed successfully. Result saved to {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
