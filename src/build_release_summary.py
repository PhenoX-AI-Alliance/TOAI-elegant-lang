import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

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
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers(repo_path):
    papers = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if 'whitepaper' in file.lower() or file.endswith('.md'):
                papers.append(os.path.join(root, file))
    return papers

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("Git repository not initialized. Initializing for release summary...")
        try:
            subprocess.run(['git', '-C', repo_path, 'init'], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.name', 'TOAI Executor'], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.email', 'executor@toai.local'], check=True)
            subprocess.run(['git', '-C', repo_path, 'add', '.'], check=True)
            subprocess.run(['git', '-C', repo_path, 'commit', '-m', 'Initial commit for release summary'], check=True)
        except Exception as init_err:
            print(f"Warning during git init: {init_err}")

    logs = get_git_log(repo_path)
    whitepapers = scan_whitepapers(repo_path)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "git_logs": logs,
        "whitepapers_found": whitepapers
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built and saved to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
