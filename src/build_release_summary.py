import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        return "Git repository not initialized."
    try:
        cmd = ['git', '-C', repo_dir, 'log', f'-n', str(max_count), '--oneline']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error fetching git log: {e}"

def scan_whitepaper():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    candidates = ['WHITE_PAPER.md', 'CONSTITUTION.md', 'README.md']
    summary = {}
    for c in candidates:
        path = os.path.join(repo_dir, c)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    summary[c] = "".join(lines[:10]).strip()
            except Exception as ex:
                summary[c] = f"Error reading file: {ex}"
    return summary

def main():
    try:
        print("Starting release summary build...")
        git_log = get_git_log(15)
        whitepaper_summary = scan_whitepaper()
        
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_log.splitlines() if git_log else [],
            "whitepaper_snippets": whitepaper_summary
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
