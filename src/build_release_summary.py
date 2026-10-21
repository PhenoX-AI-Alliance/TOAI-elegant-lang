import sys
import os
import subprocess
import json
import glob
from datetime import datetime

def main():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    git_logs = "No git history available."
    if os.path.exists(os.path.join(repo_dir, '.git')):
        try:
            result = subprocess.run(
                ['git', 'log', '-n', '10', '--oneline'],
                cwd=repo_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_logs = result.stdout
        except Exception as e:
            git_logs = f"Failed to fetch git log: {e}"
    
    whitepapers = []
    wp_pattern = os.path.join(repo_dir, '**', '*.md')
    for filepath in glob.glob(wp_pattern, recursive=True):
        if 'node_modules' in filepath or '.git' in filepath:
            continue
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                whitepapers.append({
                    'path': os.path.relpath(filepath, repo_dir),
                    'title': first_line if first_line else 'Untitled'
                })
        except Exception:
            pass
            
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_logs.splitlines(),
        "whitepapers_scanned": whitepapers[:20]
    }
    
    output_path = os.path.join(repo_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(f"Error during release summary build: {ex}", file=sys.stderr)
        sys.exit(1)