import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_path = os.path.join(repo_dir, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_path, '.git')):
        return "No git repository found at " + git_path
    
    try:
        result = subprocess.run(
            ['git', '-C', git_path, 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to fetch git log: {str(e)}"

def scan_whitepaper():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(repo_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:500] + "... [truncated]"
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    print("Building release summary...")
    git_logs = run_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_recent_commits": git_logs,
        "whitepaper_overview": whitepaper_snippet
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, 'release_summary.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)