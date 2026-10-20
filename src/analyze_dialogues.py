import sys
import os
import traceback
import time
import json

def audit_dialogues():
    corpus_path = '/home/phenox/gemini-sandbox/corpus/dialogues.jsonl'
    if not os.path.exists(corpus_path):
        print(f"Error: Corpus file not found at {corpus_path}")
        sys.exit(1)
        
    dialogues = {}
    total_lines = 0
    parse_errors = 0
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                d_id = data.get('dialogue_id')
                if d_id not in dialogues:
                    dialogues[d_id] = []
                dialogues[d_id].append(data)
            except json.JSONDecodeError:
                parse_errors += 1
                print(f"Warning: JSON decode error at line {line_num}")
                
    integrity_issues = 0
    for d_id, turns in dialogues.items():
        expected_speaker = 'user'
        for turn in turns:
            speaker = turn.get('speaker')
            if speaker != expected_speaker:
                print(f"Integrity warning in dialogue {d_id}: expected speaker '{expected_speaker}', got '{speaker}'")
                integrity_issues += 1
            expected_speaker = 'assistant' if expected_speaker == 'user' else 'user'
            
    report = {
        "total_lines": total_lines,
        "parse_errors": parse_errors,
        "total_dialogues": len(dialogues),
        "integrity_issues": integrity_issues,
        "status": "success" if parse_errors == 0 and integrity_issues == 0 else "warnings_found"
    }
    
    report_path = '/home/phenox/gemini-sandbox/TOAI_Generated/audit_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(f"Audit completed successfully. Report saved to {report_path}")

if __name__ == '__main__':
    try:
        audit_dialogues()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
