import sys
import os
import traceback
import time
import json
import collections

def analyze():
    corpus_dir = "/home/phenox/gemini-sandbox/corpus"
    os.makedirs(corpus_dir, exist_ok=True)
    corpus_path = os.path.join(corpus_dir, "dialogues.jsonl")
    
    if not os.path.exists(corpus_path):
        sample_data = [
            {"speaker": "Gaia", "text": "Hello, welcome to the Earth of Life ecosystem."},
            {"speaker": "Human", "text": "Thank you, I am glad to collaborate with you."},
            {"speaker": "Gaia", "text": "Let us build robust and warm solutions together."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                speaker = record.get("speaker", "Unknown")
                text = record.get("text", "")
                
                speaker_counts[speaker] += 1
                
                words = text.lower().split()
                for word in words:
                    cleaned_word = "".join(ch for ch in word if ch.isalnum())
                    if cleaned_word:
                        word_counts[cleaned_word] += 1
        
        result = {
            "speaker_counts": dict(speaker_counts),
            "top_words": dict(word_counts.most_common(10))
        }
        
        output_result_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_result.json"
        os.makedirs(os.path.dirname(output_result_path), exist_ok=True)
        with open(output_result_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, indent=2, ensure_ascii=False)
            
        print("Analysis completed successfully. Result saved to:", output_result_path)
    except Exception as e:
        print("Error during dialogue analysis:", str(e))
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze()
