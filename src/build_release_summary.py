import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    git_log = "No git repository found or git command failed."
    if os.path.exists(os.path.join(repo_dir, '.git')):
        try:
            result = subprocess.run(
                ['git', '-C', repo_dir, 'log', '-n', '10', '--oneline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_log = result.stdout
        except Exception as e:
            git_log = f"Failed to fetch git log: {str(e)}"
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_log.splitlines(),
        "status": "release summary generated successfully"
    }
    
    output_path = os.path.join(repo_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
