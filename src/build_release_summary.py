import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_log():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Warning: .git directory not found. Skipping git log.")
        return "No git repository found."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {e}"

def scan_whitepaper():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:20])
        except Exception as e:
            return f"Error reading whitepaper: {e}"
    return "Whitepaper not found."

def main():
    try:
        git_logs = run_git_log()
        whitepaper_snippet = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_logs.splitlines(),
            "whitepaper_overview": whitepaper_snippet
        }
        
        output_path = os.path.join(os.path.dirname(__file__), 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"Release summary successfully generated at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
