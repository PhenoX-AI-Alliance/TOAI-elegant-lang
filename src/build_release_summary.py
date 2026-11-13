import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    candidates = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    found_info = {}
    for c in candidates:
        path = os.path.join(repo_path, c)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                found_info[c] = f.readline().strip()
        else:
            found_info[c] = "Not found"
    return found_info

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    logs = get_git_log(repo_path)
    whitepapers = scan_whitepaper(repo_path)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": logs,
        "documents": whitepapers
    }
    
    output_path = os.path.join(repo_path, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
