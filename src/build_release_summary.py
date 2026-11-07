import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(git_dir):
        git_dir = repo_path
    
    cmd = ['git', '-C', git_dir, 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        return [f"Git log retrieval failed: {e}"]
    except Exception as e:
        return [f"Unexpected error in git log: {e}"]

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'src')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    logs = run_git_log()
    
    summary_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "recent_commits": logs,
        "ecosystem": "Gaia Ecosystem - TOAI Elegant Lang"
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        print(f"Failed to write release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
