import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not initialized."
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Failed to retrieve git log: {e.stderr}"

def scan_whitepaper(repo_path):
    possible_paths = [
        os.path.join(repo_path, 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'README.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:2000] # Return first 2000 chars as summary
            except Exception as e:
                return f"Error reading document {path}: {str(e)}"
    return "No whitepaper or README found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    
    os.makedirs(output_dir, exist_ok=True)
    
    git_log_data = get_git_log(repo_path)
    whitepaper_data = scan_whitepaper(repo_path)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_log": git_log_data,
        "whitepaper_summary": whitepaper_data
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        print(f"Failed to write summary file: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
