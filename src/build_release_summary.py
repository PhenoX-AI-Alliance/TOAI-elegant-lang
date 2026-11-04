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

def scan_whitepaper(repo_path):
    whitepaper_candidates = ['WHITEPAPER.md', 'README.md', 'CONSTITUTION.md']
    summary_data = {}
    for filename in whitepaper_candidates:
        filepath = os.path.join(repo_path, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary_data[filename] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                summary_data[filename] = f"Error reading file: {str(e)}"
    return summary_data

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_commits = []
    if os.path.exists(os.path.join(repo_path, '.git')):
        git_commits = get_git_log(repo_path)
    else:
        git_commits = ["Git repository not initialized or not found."]
        
    whitepaper_summary = scan_whitepaper(repo_path)
    
    release_info = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_recent_commits": git_commits,
        "documentation_summary": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
