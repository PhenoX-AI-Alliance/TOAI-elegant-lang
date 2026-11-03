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
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper(base_path):
    whitepaper_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if 'whitepaper' in file.lower() or file.endswith('.md'):
                whitepaper_files.append(os.path.join(root, file))
    return whitepaper_files

def main():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(base_dir, 'TOAI-elegant-lang')
    output_dir = os.path.join(base_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    print("Scanning repository and generating release summary...")
    git_logs = get_git_log(repo_path)
    whitepapers = scan_whitepaper(base_dir)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepapers_found": whitepapers
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)