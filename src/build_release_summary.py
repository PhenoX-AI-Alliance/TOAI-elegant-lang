import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=10):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def scan_whitepaper(repo_path):
    wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                return "\n".join(lines[:20])
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print(f"Warning: {repo_path} is not a git repository. Skipping git log.")
        git_logs = "No git repository initialized."
    else:
        git_logs = get_git_log(repo_path)
        
    whitepaper_summary = scan_whitepaper(repo_path)
    
    release_info = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        print(f"Failed to write release summary: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
