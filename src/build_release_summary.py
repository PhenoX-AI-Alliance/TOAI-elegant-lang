import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_logs():
    try:
        cmd = ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return "".join(lines[:20])
        except Exception as e:
            return f"Failed to read whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    try:
        logs = get_git_logs()
        whitepaper_snippet = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "recent_commits": logs,
            "whitepaper_overview": whitepaper_snippet
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        out_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, 'release_summary.json')
        
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at {out_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
