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
    whitepaper_path = os.path.join(workspace, 'TOAI-elegant-lang', 'docs', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[:20])
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        logs = get_git_log()
        whitepaper_summary = scan_whitepaper(workspace)
        
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "git_recent_commits": logs,
            "whitepaper_excerpt": whitepaper_summary,
            "release_status": "Stable",
            "message": "Generated with altruistic dedication by TOAI executor."
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        out_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {out_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
