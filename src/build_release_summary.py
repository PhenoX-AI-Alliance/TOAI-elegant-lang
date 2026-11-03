import sys
import os
import subprocess
import json
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
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    candidates = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'TOAI-elegant-lang', 'WHITE_PAPER.md'),
        os.path.join(workspace, 'docs', 'WHITE_PAPER.md')
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                return "".join(lines[:30])
            except Exception as e:
                return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    print("Generating release summary...")
    logs = get_git_log()
    whitepaper_intro = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepaper_snippet": whitepaper_intro
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)