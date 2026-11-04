import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Failed to fetch git log: {e}")
        return []

def scan_whitepapers(repo_path):
    papers = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if 'whitepaper' in file.lower() or 'summary' in file.lower() or file.endswith('.md'):
                papers.append(os.path.join(root, file))
    return papers

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_commits = []
    if os.path.exists(os.path.join(repo_path, '.git')):
        git_commits = get_git_log(repo_path)
    else:
        print("Git repository not initialized or found at target path.")
        
    whitepapers = scan_whitepapers(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_commits,
        "related_documents": whitepapers
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
