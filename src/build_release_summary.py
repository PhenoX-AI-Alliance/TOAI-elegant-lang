import sys
import os
import subprocess
import json
import traceback
from datetime import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not initialized."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if not os.path.exists(whitepaper_path):
        return "WHITEPAPER.md not found."
    try:
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return "".join(lines[:20])
    except Exception as e:
        return f"Failed to read whitepaper: {str(e)}"

def generate_release_summary():
    try:
        git_info = run_git_log()
        whitepaper_info = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "git_recent_commits": git_info,
            "whitepaper_excerpt": whitepaper_info
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as out:
            json.dump(summary, out, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    generate_release_summary()
