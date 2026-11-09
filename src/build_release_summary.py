import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log():
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        target_repo = os.path.join(repo_dir, 'TOAI-elegant-lang')
        if not os.path.isdir(os.path.join(target_repo, '.git')):
            return "Git repository not found or not initialized."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=target_repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_log = get_git_log()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "project": "TOAI-elegant-lang",
            "git_log": git_log,
            "status": "success",
            "message": "Release summary successfully generated with altruistic care."
        }
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
