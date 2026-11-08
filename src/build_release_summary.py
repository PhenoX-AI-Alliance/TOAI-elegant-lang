import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        git_log = []
        if os.path.exists(os.path.join(repo_path, '.git')):
            try:
                result = subprocess.run(
                    ['git', '-C', repo_path, 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                git_log = result.stdout.splitlines()
            except Exception as e:
                git_log = [f"Could not retrieve git log: {str(e)}"]
        else:
            git_log = ["Not a git repository or git not initialized."]
            
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "git_recent_commits": git_log,
            "status": "release summary generated successfully"
        }
        
        output_path = os.path.join(repo_path, 'src', 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
