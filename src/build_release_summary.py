import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("Warning: Not a git repository, skipping git log.")
        return []
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Error fetching git log: {e}")
        return []

def scan_whitepaper():
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    whitepaper_candidates = ['WHITE_PAPER.md', 'CONSTITUTION.md', 'README.md']
    summary = {}
    for candidate in whitepaper_candidates:
        full_path = os.path.join(repo_path, candidate)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[candidate] = content[:200].replace('\n', ' ')
            except Exception as e:
                summary[candidate] = f"Error reading: {e}"
        else:
            summary[candidate] = "Not found"
    return summary

def main():
    print("Building release summary...")
    git_logs = run_git_log()
    whitepaper_summary = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_path = os.path.join(output_dir, 'TOAI_Generated', 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()