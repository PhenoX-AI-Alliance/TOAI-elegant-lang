import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    git_logs = []
    if os.path.exists(os.path.join(repo_path, '.git')):
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
                capture_output=True,
                text=True,
                check=True
            )
            git_logs = result.stdout.splitlines()
        except subprocess.CalledProcessError as e:
            git_logs = [f"Git log retrieval failed: {e}"]
    else:
        git_logs = ["Repository is not a git repository or git not initialized."]
        
    whitepaper_content = ""
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:1000]
        except Exception as e:
            whitepaper_content = f"Failed to read whitepaper: {e}"
    else:
        whitepaper_content = "Whitepaper not found."
        
    summary_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "version_overview": "TOAI-elegant-lang Release Summary",
        "git_recent_commits": git_logs,
        "whitepaper_snippet": whitepaper_content
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
