import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_log = "No git history available."
    if os.path.exists(os.path.join(repo_path, '.git')):
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_log = result.stdout
        except Exception as e:
            git_log = f"Failed to fetch git log: {str(e)}"
    
    whitepaper_content = "Whitepaper not found."
    wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:1000]
        except Exception as e:
            whitepaper_content = f"Failed to read whitepaper: {str(e)}"
            
    summary_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_recent_commits": git_log.splitlines(),
        "whitepaper_snippet": whitepaper_content
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
