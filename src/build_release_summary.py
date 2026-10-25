# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import datetime
import traceback

def get_git_log(max_count=10):
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        return ["Git repository not initialized or not found."]
    try:
        cmd = ['git', '-C', repo_dir, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepapers():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    docs_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    found_files = []
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    found_files.append(os.path.join(root, file))
    return found_files

def main():
    try:
        print("Starting release summary generation...")
        git_logs = get_git_log(15)
        whitepapers = scan_whitepapers()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_logs,
            "whitepapers_scanned": whitepapers
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
