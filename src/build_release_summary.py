import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_command(cmd, cwd):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(cmd)}")
        print(e.stderr)
        return ""
    except Exception as e:
        print(f"Unexpected error running git: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}")
        sys.exit(1)
        
    git_check = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_check):
        print(f"Not a git repository: {repo_dir}")
        sys.exit(1)
        
    print("Gathering git log...")
    git_log = run_git_command(['git', 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'], repo_dir)
    
    print("Searching for whitepapers or documentation...")
    docs = []
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith('.md') or file.endswith('.txt'):
                docs.append(os.path.join(root, file))
                
    summary_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "recent_commits": git_log.splitlines() if git_log else [],
        "documentation_files": docs
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)