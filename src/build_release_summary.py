# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    candidates = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    found = {}
    for c in candidates:
        if os.path.exists(c):
            with open(c, 'r', encoding='utf-8') as f:
                found[c] = f.read()[:500]
    return found

def main():
    print("Building release summary...")
    logs = get_git_log()
    papers = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepaper_snippets": list(papers.keys()),
        "status": "ready"
    }
    
    out_path = "release_summary.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at {out_path}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
