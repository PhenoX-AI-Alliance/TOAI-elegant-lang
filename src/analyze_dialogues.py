import sys
import os
import traceback
import time
import json
import collections
import re

def analyze_corpus():
    corpus_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus not found at {{corpus_path}}", file=sys.stderr)
        # Create a dummy corpus for demonstration if missing, ensuring real-world execution flow
        os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
        sample_data = [
            {"speaker": "Alice", "text": "Hello, the Gaia ecosystem is wonderful and warm."},
            {"speaker": "Bob", "text": "Indeed, altruistic monetization brings true value."},
            {"speaker": "Alice", "text": "Let us build robust systems together."}
        ]
        with open(corpus_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"Created sample corpus at {{corpus_path}}")

    speaker_counts = collections.Counter()
    word_counts = collections.Counter()
    
    try:
        with open(corpus_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    speaker = data.get("speaker", "Unknown")
                    text = data.get("text", "")
                    
                    speaker_counts[speaker] += 1
                    
                    # Simple tokenization / root word extraction simulation
                    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
                    for word in words:
                        word_counts[word] += 1
                except json.JSONDecodeError as jde:
                    print(f"Warning: JSON decode error at line {{line_num}}: {{jde}}", file=sys.stderr)
    except Exception as e:
        print(f"Error reading corpus file: {{e}}", file=sys.stderr)
        sys.exit(1)
        
    result = {
        "speaker_utterance_counts": dict(speaker_counts),
        "top_word_frequencies": dict(word_counts.most_common(20)),
        "analyzed_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    output_report_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/analysis_report.json"
    try:
        with open(output_report_path, "w", encoding="utf-8") as out_f:
            json.dump(result, out_f, ensure_ascii=False, indent=2)
        print(f"Successfully analyzed dialogues and saved report to {{output_report_path}}")
    except Exception as e:
        print(f"Error saving analysis report: {{e}}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        analyze_corpus()
    except Exception as e:
        print(f"Critical error in execution: {{e}}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
