import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {str(e)}"

def generate_release_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_history = get_git_log()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary_data = {
        "timestamp": timestamp,
        "version": "1.0.0",
        "git_recent_commits": git_history,
        "ecosystem": "Gaia Ecosystem - Earth of Life"
    }
    
    summary_path = os.path.join(output_dir, 'release_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=4, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {summary_path}")

if __name__ == '__main__':
    try:
        generate_release_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
