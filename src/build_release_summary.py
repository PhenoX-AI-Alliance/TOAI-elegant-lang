import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_log():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            return "Git repository not found."
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = run_git_log()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "version_overview": "TOAI-elegant-lang Release Summary",
            "git_recent_commits": git_logs.splitlines(),
            "status": "success"
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
