import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_command(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return res.stdout.strip()
    except Exception as e:
        print(f"Git command error: {e}")
        return ""

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory not found: {repo_dir}")
        sys.exit(1)
        
    os.chdir(repo_dir)
    
    git_log = run_git_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'])
    latest_tag = run_git_command(['git', 'describe', '--tags', '--abbrev=0'])
    if not latest_tag:
        latest_tag = "v0.1.0"
        
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "latest_tag": latest_tag,
        "recent_commits": git_log.splitlines() if git_log else []
    }
    
    output_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
