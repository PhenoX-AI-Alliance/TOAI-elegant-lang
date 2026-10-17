# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace):
    whitepaper_path = os.path.join(workspace, 'WHITE_PAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[:20])
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_commits = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace)
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_commits,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    summary_path = os.path.join(output_dir, 'release_summary.json')
    try:
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {summary_path}")
    except Exception as e:
        print(f"Failed to write release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
