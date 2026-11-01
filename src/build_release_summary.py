import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=10):
    try:
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return "Git repository not initialized."
        
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error retrieving git log: {str(e)}"

def scan_whitepaper(workspace_path):
    whitepaper_path = os.path.join(workspace_path, 'TOAI-elegant-lang', 'docs', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:500] + "... [truncated]"
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("Scanning Git Log...")
    git_log = get_git_log(repo_path)
    
    print("Scanning Whitepaper...")
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "git_log": git_log,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
