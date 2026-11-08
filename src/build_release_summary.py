import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper(repo_path):
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                return f.read()[:1000]
        except Exception as e:
            print(f"Warning: Could not read whitepaper: {e}")
    return "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.abspath(os.path.join(workspace_dir, 'TOAI-elegant-lang'))
    
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        try:
            subprocess.run(['git', 'init', repo_path], check=True)
        except Exception as e:
            print(f"Error initializing git repo: {e}")
            sys.exit(1)
            
    git_logs = get_git_log(repo_path)
    whitepaper_snippet = scan_whitepaper(repo_path)
    
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_logs": git_logs,
        "whitepaper_snippet": whitepaper_snippet
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
