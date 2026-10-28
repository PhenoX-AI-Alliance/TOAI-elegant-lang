# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_path = os.path.join(repo_dir, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(git_path, '.git')):
            git_path = repo_dir
            
        cmd = ['git', '-C', git_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ad : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log acquisition failed: {str(e)}"]

def scan_whitepaper():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        wp_candidates = [
            os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
            os.path.join(workspace_dir, 'WHITEPAPER.md')
        ]
        for path in wp_candidates:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    return ''.join(lines[:20]) # First 20 lines as summary
        return "Whitepaper not found."
    except Exception as e:
        return f"Whitepaper scan failed: {str(e)}"

def build_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    now = datetime.datetime.now().isoformat()
    git_logs = get_git_log(15)
    whitepaper_snippet = scan_whitepaper()
    
    summary_data = {
        "timestamp": now,
        "version": "1.0.0-alpha",
        "git_recent_commits": git_logs,
        "whitepaper_overview": whitepaper_snippet
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    md_file = os.path.join(output_dir, 'RELEASE_NOTE.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# TOAI Release Summary\n\n")
        f.write(f"Generated at: {now}\n\n")
        f.write(f"## Whitepaper Overview\n\n{whitepaper_snippet}\n\n")
        f.write(f"## Recent Changes (Git Log)\n\n")
        for log in git_logs:
            f.write(f"- {log}\n")
            
    print(f"Successfully generated release summary at {out_file} and {md_file}")

if __name__ == '__main__':
    try:
        build_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
