import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("[INFO] Starting release summary generation...")
    
    git_logs = "No git history available."
    if os.path.exists(os.path.join(repo_path, '.git')):
        try:
            result = subprocess.run(
                ['git', 'log', '-n', '10', '--oneline'],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            git_logs = result.stdout
        except Exception as e:
            git_logs = f"Error fetching git log: {e}"
    else:
        print("[WARNING] Target directory is not a git repository.")

    whitepaper_path = os.path.join(workspace_dir, 'WHITE_PAPER.md')
    whitepaper_content = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:2000] # Read first 2000 chars
        except Exception as e:
            whitepaper_content = f"Error reading whitepaper: {e}"

    summary_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_recent_commits": git_logs.splitlines(),
        "whitepaper_excerpt": whitepaper_content
    }

    output_file = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"[SUCCESS] Release summary successfully written to {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
