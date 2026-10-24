import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_log(max_count=10):
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            return ["No git repository found at " + repo_dir]
        cmd = ['git', '-C', repo_dir, 'log', f'-n{max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        wp_path = os.path.join(repo_dir, 'WHITE_PAPER.md')
        if os.path.exists(wp_path):
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[:30]) # Return first 30 lines as summary
        return "Whitepaper not found."
    except Exception as e:
        return f"Error reading whitepaper: {str(e)}"

def generate_release_summary():
    logs = run_git_log(15)
    wp_summary = scan_whitepaper()
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": logs,
        "whitepaper_excerpt": wp_summary
    }
    
    output_path = os.path.join(os.path.dirname(__file__), 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    generate_release_summary()
