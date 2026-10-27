# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import datetime
import traceback

def get_git_log(repo_path, max_count=10):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not initialized."
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper(workspace_path):
    candidates = ['whitepaper.md', 'README.md', 'CONSTITUTION.md']
    found_data = {}
    for c in candidates:
        full_path = os.path.join(workspace_path, c)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    found_data[c] = f.read()[:500]
            except Exception as e:
                found_data[c] = f"Error reading: {str(e)}"
    return found_data

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("Scanning Git logs...")
    git_logs = get_git_log(repo_path)
    
    print("Scanning documentation...")
    docs = scan_whitepaper(workspace_dir)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": git_logs,
        "documents": list(docs.keys())
    }
    
    output_file = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
