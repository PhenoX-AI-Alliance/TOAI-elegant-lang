import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            return "No git repository found."
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
        return f"Could not retrieve git log: {str(e)}"

def build_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_log_data = get_git_log()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary = {
        "timestamp": timestamp,
        "version_overview": "TOAI Elegant Lang Release Summary - Gaia Ecosystem",
        "git_recent_commits": git_log_data.splitlines()
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at: {output_file}")

if __name__ == '__main__':
    try:
        build_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
