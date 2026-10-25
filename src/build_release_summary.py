#!/usr/bin/env python3
import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        return ["Git repository not initialized or not found."]
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        return [f"Error fetching git log: {e.stderr}"]

def scan_whitepapers():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    docs_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    papers = []
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    papers.append(os.path.join(root, file))
    return papers

def main():
    print("Building release summary...")
    logs = get_git_log(15)
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "scanned_documents": papers
    }
    
    output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n