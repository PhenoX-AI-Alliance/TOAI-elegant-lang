import sys
import os
import traceback
import subprocess
import json
import datetime

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            
        git_log = ""
        try:
            if os.path.exists(os.path.join(repo_path, '.git')):
                result = subprocess.run(
                    ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                git_log = result.stdout
            else:
                git_log = "Git repository not initialized or not found."
        except Exception as e:
            git_log = f"Failed to fetch git log: {str(e)}"
            
        summary_data = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "git_recent_commits": git_log.splitlines(),
            "status": "release summary generated successfully"
        }
        
        output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully written to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()