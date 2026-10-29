# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not initialized."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepapers():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_files = []
    for root, dirs, files in os.walk(repo_path):
        for f in files:
            if 'whitepaper' in f.lower() or f.endswith('.md'):
                wp_files.append(os.path.join(root, f))
    return wp_files[:5]

def generate_release_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = run_git_log()
    whitepapers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_logs,
        "related_documents": whitepapers,
        "version": "1.0.0",
        "status": "release_summary_generated"
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {out_file}")

if __name__ == '__main__':
    try:
        generate_release_summary()
    except Exception as e:
        print(f"Error in release summary generation: {e}", file=sys.stderr)
        sys.exit(1)
