import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not initialized or found."
    
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing git log: {e}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_path = os.path.join(repo_path, 'WHITE_PAPER.md')
    if not os.path.exists(whitepaper_path):
        return "Whitepaper not found."
    
    try:
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return "".join(lines[:20])
    except Exception as e:
        return f"Error reading whitepaper: {e}"

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_summary = run_git_log()
        whitepaper_summary = scan_whitepaper()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "git_log": git_summary,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
