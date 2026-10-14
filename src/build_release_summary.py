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
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace):
    whitepaper_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return "".join(lines[:20])
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    release_dir = os.path.join(workspace, 'TOAI_Generated', 'releases')
    os.makedirs(release_dir, exist_ok=True)
    
    git_history = get_git_log()
    whitepaper_snippet = scan_whitepaper(workspace)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_history,
        "whitepaper_overview": whitepaper_snippet,
        "status": "SUCCESS",
        "message": "Release summary successfully generated with altruistic care."
    }
    
    output_file = os.path.join(release_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
        
    print(f"Release summary successfully written to {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)