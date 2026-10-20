# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    candidates = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'CONSTITUTION.md'),
        os.path.join(workspace_dir, 'README.md')
    ]
    summary = {}
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:300] + "..." if len(content) > 300 else content
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading file: {str(e)}"
    return summary

def main():
    try:
        print("Starting TOAI Release Summary Generation...")
        git_history = get_git_log(15)
        whitepaper_info = scan_whitepaper()
        
        release_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0-gaia",
            "git_recent_commits": git_history,
            "whitepaper_snippets": whitepaper_info
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        out_file = os.path.join(output_dir, 'release_summary.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {out_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
