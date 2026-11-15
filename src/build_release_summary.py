import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_command(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command error: {e.stderr.strip()}", file=sys.stderr)
        return ""

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Error: Repository directory not found at {repo_dir}", file=sys.stderr)
        sys.exit(1)
        
    git_check = run_command(['git', 'rev-parse', '--is-inside-work-tree'], cwd=repo_dir)
    if git_check != 'true':
        print("Error: Not inside a valid git repository.", file=sys.stderr)
        sys.exit(1)
        
    git_log = run_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'], cwd=repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_summary = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            whitepaper_summary = "".join(lines[:20])
            
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": git_log.splitlines() if git_log else [],
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
