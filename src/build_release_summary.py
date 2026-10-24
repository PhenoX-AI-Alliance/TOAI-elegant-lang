# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'))
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        with open(wp_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [line.strip() for line in lines[:20] if line.strip()]
    return ["Whitepaper not found."]

def main():
    print("Building Release Summary...")
    logs = get_git_log(15)
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": logs,
        "whitepaper_overview": whitepaper_snippet
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
