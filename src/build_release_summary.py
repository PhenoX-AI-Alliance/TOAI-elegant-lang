import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepapers(base_dir):
    whitepapers = []
    try:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    whitepapers.append(full_path)
    except Exception as e:
        print(f"Warning: Could not scan whitepapers: {e}")
    return whitepapers

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        try:
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
        except Exception as e:
            print(f"Git init failed: {e}")

    git_logs = get_git_log(repo_path)
    whitepapers = scan_whitepapers(workspace)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_commits": git_logs,
        "discovered_documents": whitepapers,
        "status": "success"
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
