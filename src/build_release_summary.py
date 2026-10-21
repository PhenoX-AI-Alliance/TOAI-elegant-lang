# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(limit=10):
    try:
        cmd = ['git', 'log', f'-n {limit}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_candidates = [
        os.path.join(workspace, 'WHITEPAPER.md'),
        os.path.join(workspace, 'CONSTITUTION.md'),
        os.path.join(workspace, 'README.md')
    ]
    summary = {}
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    title = lines[0].strip() if lines else "No Title"
                    summary[os.path.basename(path)] = title
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading: {str(e)}"
    return summary

def main():
    print("=== TOAI Release Summary Builder ===")
    logs = get_git_log()
    papers = scan_whitepaper()
    
    release_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": logs,
        "documents": papers
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
