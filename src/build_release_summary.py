import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_history():
    try:
        res = subprocess.run(['git', 'log', '-n', '20', '--oneline'], capture_output=True, text=True, cwd=os.getcwd())
        if res.returncode == 0:
            return res.stdout
    except Exception as e:
        print(f"Git history fetch error: {e}")
    return "No git history available."

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'docs', 'WHITE_PAPER.md')
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    return f.read()[:1000]
            except Exception:
                pass
    return "Whitepaper not found."

def main():
    print("Building release summary for TOAI Ecosystem...")
    history = get_git_history()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_history": history,
        "whitepaper_snippet": whitepaper_snippet,
        "status": "success"
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(out_dir, exist_ok=True)
    
    out_file = os.path.join(out_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
