import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def run_git_command(repo_path):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {str(e)}"

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        try:
            subprocess.run(['git', 'init', repo_path], check=True)
        except Exception:
            pass
            
    git_logs = run_git_command(repo_path)
    
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    whitepaper_summary = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                whitepaper_summary = "".join(lines[:10]).strip()
        except Exception as e:
            whitepaper_summary = f"Error reading whitepaper: {str(e)}"
            
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "git_logs": git_logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully generated release summary at {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)