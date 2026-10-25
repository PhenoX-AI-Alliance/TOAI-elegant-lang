#!/usr/bin/env python3
import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            return ["No git repository found at target path."]
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    candidates = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    found_info = {}
    for c in candidates:
        path = os.path.join(repo_dir, c)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    found_info[c] = f.readline().strip()
            except Exception:
                found_info[c] = "Unable to read"
    return found_info

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        logs = get_git_log(15)
        whitepaper_info = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "version_summary": "TOAI-elegant-lang Release Summary",
            "git_history": logs,
            "documents": whitepaper_info
        }
        
        out_file = os.path.join(output_dir, 'release_summary.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {out_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
