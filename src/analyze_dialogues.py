import sys
import os
import traceback
import time
import json
import collections
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_freqs = collections.defaultdict(lambda: collections.defaultdict(int))
    
    print("Reading corpus and analyzing dialogues...")
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
                    
                    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
                    for word in words:
                        word_freqs[speaker][word] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {line_num}: {jde}")
                except Exception as ex:
                    print(f"Warning: Error processing line {line_num}: {ex}")
                    
        result = {
            "speaker_utterances": dict(speaker_counts),
            "speaker_word_frequencies": {sp: dict(freqs.most_common(20)) for sp, freqs in word_freqs.items()}
        }
        
        output_result_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/src/dialogue_analysis_result.json"
        with open(output_result_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
            
        print(f"Analysis complete. Results successfully saved to {output_result_path}")
        
    except Exception as e:
        print(f"Critical error during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    analyze_corpus()
