import sys
import os
import traceback
import time
import json
import collections
import re

def analyze_dialogues():
    corpus_path = "/home/phenox/gemini-sandbox/corpus/dialogues.jsonl"
    output_report_path = "/home/phenox/gemini-sandbox/TOAI_Generated/dialogue_analysis_report.json"
    
    os.makedirs(os.path.dirname(output_report_path), exist_ok=True)
    
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Corpus file not found at {corpus_path}")
        
    speaker_counts = collections.defaultdict(int)
    word_counts = collections.defaultdict(int)
    
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
                
                words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
                for word in words:
                    word_counts[word] += 1
            except json.JSONDecodeError:
                continue
                
    report = {
        "timestamp": time.time(),
        "speaker_utterance_counts": dict(speaker_counts),
        "top_words": dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20])
    }
    
    with open(output_report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully analyzed dialogues. Report saved to {output_report_path}")

if __name__ == "__main__":
    try:
        analyze_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
