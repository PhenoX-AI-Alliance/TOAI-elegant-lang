# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=20):
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return "Git repository not initialized."
        cmd = ["git", "log", f"-n", str(max_count), "--pretty=format:%h - %an, %ar : %s"]
        result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Could not retrieve git log: {e}"

def scan_whitepaper():
    candidates = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'WHITE_PAPER.md')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'README.md'))
    ]
    summary = {}
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading file: {e}"
    return summary

def main():
    print("Generating Release Summary...")
    git_logs = get_git_log(30)
    whitepaper_data = scan_whitepaper()
    
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_history": git_logs.splitlines(),
        "whitepaper_snippets": whitepaper_data
    }
    
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'release_summary.json'))
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {out_path}")
    except Exception as e:
        print(f"Failed to write release summary: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
