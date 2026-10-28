# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if 'whitepaper' in file.lower() or 'doc' in file.lower() or file.endswith('.md'):
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        pass
    return whitepaper_files

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    print(f"Scanning workspace: {workspace_dir}")
    
    git_history = get_git_log(15)
    docs = scan_whitepaper(workspace_dir)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": git_history,
        "related_documents": docs[:20]
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'src', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    main()
