import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_candidates = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'README.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read(4000) # Read first 4000 chars
                    return path, content
            except Exception as e:
                pass
    return None, "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_history = []
    if os.path.exists(os.path.join(repo_path, '.git')):
        git_history = get_git_log(repo_path)
    else:
        print("Warning: .git directory not found. Initializing repository or skipping git log.")
        try:
            subprocess.run(['git', 'init', repo_path], capture_output=True, text=True, check=True)
            git_history = get_git_log(repo_path)
        except Exception as e:
            git_history = [f"Git init failed: {str(e)}"]

    wp_path, wp_content = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "repository": "TOAI-elegant-lang",
        "whitepaper_path": wp_path,
        "whitepaper_snippet": wp_content[:500] if wp_content else "",
        "recent_commits": git_history
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
