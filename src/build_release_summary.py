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
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace):
    whitepaper_paths = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'TOAI_Generated', 'WHITE_PAPER.md')
    ]
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000]
            except Exception:
                pass
    return "No whitepaper found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = get_git_log()
    whitepaper_snippet = scan_whitepaper(workspace)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "recent_commits": logs,
        "whitepaper_snippet": whitepaper_snippet,
        "status": "release summary generated successfully with altruistic warmth"
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {out_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
