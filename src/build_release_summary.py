# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=20):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    docs_dir = os.path.join(workspace_dir, 'docs')
    whitepapers = []
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    whitepapers.append(os.path.join(root, file))
    return whitepapers

def main():
    print("=== TOAI Release Summary Generator ===")
    git_commits = get_git_log()
    whitepapers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": git_commits,
        "whitepapers_found": whitepapers,
        "version": "1.0.0-gaia"
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_json = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_json}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in build_release_summary: {str(e)}", file=sys.stderr)
        sys.exit(1)
