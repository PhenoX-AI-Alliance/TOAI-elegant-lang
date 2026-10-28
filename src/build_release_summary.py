# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(max_count=20):
    try:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run(
            ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        whitepaper_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:30])
        return "Whitepaper not found."
    except Exception as e:
        return f"Whitepaper scan failed: {str(e)}"

def build_summary():
    logs = get_git_log()
    whitepaper_excerpt = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0-alpha",
        "git_recent_commits": logs,
        "whitepaper_excerpt": whitepaper_excerpt
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        build_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
