import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        subprocess.run(['git', 'init'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.name', 'TOAI Executor'], cwd=repo_path, check=True)
        subprocess.run(['git', 'config', 'user.email', 'executor@toai.local'], cwd=repo_path, check=True)
        
    # Check if HEAD exists
    res = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=repo_path, capture_output=True, text=True)
    if res.returncode != 0:
        # Create an initial commit if no commits exist
        readme_path = os.path.join(repo_path, 'README.md')
        if not os.path.exists(readme_path):
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write('# TOAI Elegant Lang\nInitial release summary generator target.\n')
        subprocess.run(['git', 'add', 'README.md'], cwd=repo_path, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit', '--allow-empty'], cwd=repo_path, check=True)
        
    # Fetch git log
    log_res = subprocess.run(['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'], cwd=repo_path, capture_output=True, text=True)
    git_log_text = log_res.stdout if log_res.returncode == 0 else "No git log available."
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "git_logs": git_log_text.splitlines()
    }
    
    output_json_path = os.path.join(repo_path, 'src', 'release_summary.json')
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated release summary at {output_json_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)