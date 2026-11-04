import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=10):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if 'whitepaper' in file.lower() or 'release' in file.lower() or 'summary' in file.lower():
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error scanning files: {e}", file=sys.stderr)
    return whitepaper_files

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_commits = []
    if os.path.exists(os.path.join(repo_path, '.git')):
        git_commits = get_git_log(repo_path)
    else:
        print("Git repository not initialized at target path. Skipping git log.")
    
    whitepaper_paths = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "repository": repo_path,
        "recent_commits": git_commits,
        "relevant_documents": whitepaper_paths,
        "status": "success"
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
