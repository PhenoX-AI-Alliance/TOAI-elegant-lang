import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def run_git_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"Git command failed: {e}")
        return ""

def main():
    print("Starting release summary generation...")
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'])
    git_status = run_git_command(['git', 'status', '--porcelain'])
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else [],
        "version": "1.0.0-alpha",
        "ecosystem": "Gaia Ecosystem - Earth of Life"
    }
    
    output_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
