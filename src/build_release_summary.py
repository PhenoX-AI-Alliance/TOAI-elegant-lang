import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_paths = [
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'CONSTITUTION.md')
    ]
    summary = {}
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:500] + ('...' if len(content) > 500 else '')
            except Exception as e:
                summary[os.path.basename(path)] = f"Read error: {str(e)}"
        else:
            summary[os.path.basename(path)] = "Not found"
    return summary

def main():
    try:
        print("Starting release summary generation...")
        git_logs = get_git_log()
        whitepaper_summary = scan_whitepaper()
        
        release_info = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0-gaia",
            "git_recent_commits": git_logs,
            "whitepaper_summary": whitepaper_summary
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        target_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(target_dir, exist_ok=True)
        
        out_path = os.path.join(target_dir, 'release_summary.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {out_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
