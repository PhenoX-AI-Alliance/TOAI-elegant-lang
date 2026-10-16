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
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'TOAI-elegant-lang', 'WHITE_PAPER.md'),
        os.path.join(workspace, 'docs', 'WHITE_PAPER.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000]
            except Exception:
                pass
    return "Whitepaper not found or unreadable."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_history = get_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-alpha",
        "git_recent_commits": git_history,
        "whitepaper_summary": whitepaper_snippet,
        "message": "Gaia Ecosystem Release Summary generated successfully with altruistic intent."
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
