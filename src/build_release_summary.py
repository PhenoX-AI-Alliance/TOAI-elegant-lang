import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log acquisition failed: {str(e)}"

def scan_whitepaper(workspace_dir):
    whitepaper_candidates = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'docs', 'WHITE_PAPER.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return content[:500] + "... [Truncated]"
            except Exception as e:
                return f"Error reading whitepaper at {path}: {str(e)}"
    return "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    whitepaper_snippet = scan_whitepaper(workspace_dir)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_logs.splitlines(),
        "whitepaper_snippet": whitepaper_snippet,
        "status": "success"
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
