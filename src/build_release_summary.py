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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace_dir, 'WHITE_PAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[:20])
        except Exception as e:
            return f"Failed to read whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "git_recent_commits": logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {out_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
