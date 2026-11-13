import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    repo_path = os.path.dirname(os.path.abspath(__file__))
    git_dir = os.path.join(repo_path, '.git')
    
    # Search parent directories for .git if not in current
    current = repo_path
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, '.git')):
            repo_path = current
            break
        current = os.path.dirname(current)
        
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_files = []
    for root, dirs, files in os.walk(workspace):
        for file in files:
            if 'whitepaper' in file.lower() or file.endswith('.md'):
                wp_files.append(os.path.join(root, file))
    return wp_files[:10]

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_history = get_git_log()
        whitepapers = scan_whitepapers()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "git_log": git_history.splitlines() if git_history else [],
            "whitepapers_scanned": whitepapers
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
