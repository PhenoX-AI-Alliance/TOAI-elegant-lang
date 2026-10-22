import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    candidates = ['WHITEPAPER.md', 'README.md', 'CONSTITUTION.md']
    found = {}
    for c in candidates:
        if os.path.exists(c):
            with open(c, 'r', encoding='utf-8') as f:
                found[c] = f.readline().strip()
    return found

def main():
    print("Building release summary...")
    logs = get_git_log(15)
    wp = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_commits": logs,
        "documents": wp
    }
    
    out_path = "release_summary.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {out_path}")

if __name__ == '__main__':
    main()
