import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return "Git repository not initialized."
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error fetching git log: {e.stderr}"

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
                    return path, f.read()[:2000]
            except Exception as ex:
                return path, f"Error reading file: {str(ex)}"
    return None, "No whitepaper or main readme found."

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        git_history = get_git_log(repo_path)
        wp_path, wp_content = scan_whitepaper(repo_path)
        
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "repository": repo_path,
            "whitepaper_path": wp_path,
            "whitepaper_snippet": wp_content,
            "git_log": git_history
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
