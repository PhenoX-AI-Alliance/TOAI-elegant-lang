import sys
import os
import traceback
import time
import json
import subprocess
import datetime

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
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper(workspace_path):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(workspace_path):
            for file in files:
                if 'whitepaper' in file.lower() or 'summary' in file.lower() or 'release' in file.lower():
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Warning: Error scanning files: {e}")
    return whitepaper_files

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        try:
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
        except Exception as e:
            print(f"Notice: git init skipped or failed: {e}")
            
    git_logs = get_git_log(repo_path)
    whitepapers = scan_whitepaper(workspace_dir)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepapers_found": whitepapers,
        "version": "1.0.0"
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
