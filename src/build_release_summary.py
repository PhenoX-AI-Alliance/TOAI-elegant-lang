import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git logs: {e}")
        return []

def scan_whitepapers(repo_path):
    whitepapers = []
    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    whitepapers.append(full_path)
    except Exception as e:
        print(f"Warning: Could not scan whitepapers: {e}")
    return whitepapers

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    is_git_repo = os.path.isdir(os.path.join(repo_path, '.git'))
    git_logs = []
    if is_git_repo:
        git_logs = get_git_logs(repo_path)
    else:
        print("Notice: Target path is not a git repository. Skipping git log extraction.")
        
    whitepapers = scan_whitepapers(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "repository_path": repo_path,
        "is_git_repository": is_git_repo,
        "git_recent_commits": git_logs,
        "discovered_documents": whitepapers
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)