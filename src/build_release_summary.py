import sys
import os
import traceback
import subprocess
import json
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

def scan_whitepapers(repo_path):
    whitepapers = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if 'whitepaper' in file.lower() or file.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_path)
                whitepapers.append(rel_path)
    return whitepapers

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_commits = []
    if os.path.isdir(os.path.join(repo_path, '.git')):
        git_commits = get_git_log(repo_path)
    else:
        print("Notice: Git repository not initialized or found at target path. Skipping git log.")

    whitepapers = scan_whitepapers(repo_path)
    
    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "repository": "TOAI-elegant-lang",
        "recent_commits": git_commits,
        "whitepapers_found": whitepapers
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
