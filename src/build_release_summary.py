import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not retrieve git log: {e}")
        return []

def scan_whitepaper(repo_path):
    whitepaper_candidates = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    summary_info = {}
    for candidate in whitepaper_candidates:
        file_path = os.path.join(repo_path, candidate)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    summary_info[candidate] = [line.strip() for line in lines[:10] if line.strip()]
            except Exception as e:
                print(f"Warning: Could not read {candidate}: {e}")
    return summary_info

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        print(f"Scanning repository at: {repo_path}")
        
        git_logs = get_git_log(repo_path)
        whitepaper_data = scan_whitepaper(repo_path)
        
        release_summary = {
            "timestamp": datetime.now().isoformat(),
            "repository": "TOAI-elegant-lang",
            "recent_commits": git_logs,
            "documentation_snippets": whitepaper_data
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_summary, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully generated release summary at: {output_file}")
        
    except Exception as e:
        print(f"Error in release summary build: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
