# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace_dir):
    wp_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITESPAPER.md')
    if os.path.exists(wp_path):
        with open(wp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [line.strip() for line in lines[:20] if line.strip()]
    return ["Whitepaper not found."]

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = get_git_log(15)
    whitepaper_summary = scan_whitepaper(workspace)
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "git_logs": logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {out_file}")

if __name__ == '__main__':
    main()
