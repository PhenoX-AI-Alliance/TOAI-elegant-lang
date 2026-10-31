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
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}", file=sys.stderr)
        return []

def scan_whitepaper(workspace_path):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(workspace_path):
            for file in files:
                if 'whitepaper' in file.lower() or 'summary' in file.lower() or file.endswith('.md'):
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Warning: Error scanning files: {e}", file=sys.stderr)
    return whitepaper_files

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        try:
            os.makedirs(repo_path, exist_ok=True)
            subprocess.run(['git', 'init'], cwd=repo_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"Error initializing git repo: {e}", file=sys.stderr)
            
    git_logs = get_git_log(repo_path)
    whitepapers = scan_whitepaper(workspace)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_commits": git_logs,
        "scanned_documents": whitepapers[:10]
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        print(f"Error writing summary file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
