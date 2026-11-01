import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not found. No commit history available."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Failed to retrieve git log: {e}"

def generate_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    
    whitepaper_content = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:500] + "... [truncated]"
        except Exception as e:
            whitepaper_content = f"Error reading whitepaper: {e}"
            
    git_log = get_git_log()
    timestamp = datetime.datetime.now().isoformat()
    
    summary = {
        "timestamp": timestamp,
        "version_summary": "TOAI-elegant-lang Release Summary",
        "recent_commits": git_log,
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(summary, out, ensure_ascii=False, indent=4)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
