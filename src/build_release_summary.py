# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'docs', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            lines = content.splitlines()
            return lines[:20]
        except Exception as e:
            return [f"Whitepaper read failed: {str(e)}"]
    return ["Whitepaper not found."]

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    summary_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(summary_dir, exist_ok=True)
    
    print("Scanning repository and whitepaper for release summary...")
    logs = get_git_log(15)
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_file = os.path.join(summary_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
