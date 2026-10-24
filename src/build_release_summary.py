import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'WHITEPAPER.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                return "".join(lines[:20]) # First 20 lines as summary
            except Exception as e:
                return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_commits = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_commits,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    main()
