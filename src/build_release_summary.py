import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_path = os.path.join(repo_dir, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_path, '.git')):
        return "Git repository not initialized or path incorrect."
    try:
        cmd = ['git', '-C', git_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {e}"

def scan_whitepaper():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(repo_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
    if not os.path.exists(wp_path):
        return "White paper not found."
    try:
        with open(wp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return "".join(lines[:30])
    except Exception as e:
        return f"Failed to read white paper: {e}"

def main():
    try:
        print("Building release summary...")
        git_history = get_git_log(15)
        whitepaper_snippet = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0-gaia",
            "git_log": git_history,
            "whitepaper_overview": whitepaper_snippet
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
