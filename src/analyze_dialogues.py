import sys
import os
import traceback
import json
import collections
import re

def main():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    speaker = data.get("speaker", "unknown")
                    text = data.get("text", "")
                    
                    speaker_counts[speaker] += 1
                    
                    words = re.findall(r'\b\w+\b', text.lower())
                    for word in words:
                        word_counts[word] += 1
                except json.JSONDecodeError:
                    print(f"Warning: Failed to parse JSON at line {line_num}")
                    
        print("=== Speaker Turn Counts ===")
        for speaker, count in speaker_counts.items():
            print(f"{speaker}: {count} turns")
            
        print("\n=== Top 10 Words ===")
        for word, count in word_counts.most_common(10):
            print(f"{word}: {count}")
            
    except Exception as e:
        print(f"Error during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
