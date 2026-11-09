import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    git_logs = []
    try:
        if os.path.exists(os.path.join(repo_path, '.git')):
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_logs = result.stdout.splitlines()
        else:
            git_logs = ["Git repository not initialized or found at path."]
    except Exception as e:
        git_logs = [f"Error fetching git logs: {str(e)}"]
        
    whitepaper_content = "Whitepaper data not available."
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:1000] # Read first 1000 chars as summary
        except Exception as e:
            whitepaper_content = f"Error reading whitepaper: {str(e)}"
            
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_logs,
        "whitepaper_summary_snippet": whitepaper_content
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
