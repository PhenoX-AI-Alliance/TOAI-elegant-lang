import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=10):
    try:
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return ["Not a git repository or git not initialized."]
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_candidates = ['WHITEPAPER.md', 'README.md', 'CONSTITUTION.md']
    found_info = {}
    for candidate in whitepaper_candidates:
        file_path = os.path.join(repo_path, candidate)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    found_info[candidate] = content.strip().split('\n')[0]
            except Exception as e:
                found_info[candidate] = f"Error reading: {str(e)}"
    return found_info

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            
        git_logs = get_git_log(repo_path)
        whitepaper_info = scan_whitepaper(repo_path)
        
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "repository": "TOAI-elegant-lang",
            "git_recent_commits": git_logs,
            "whitepaper_summary": whitepaper_info
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
