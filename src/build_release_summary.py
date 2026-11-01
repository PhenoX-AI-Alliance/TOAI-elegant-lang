import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        target_repo = os.path.join(repo_path, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(target_repo, '.git')):
            return "Git repository not initialized."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=target_repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_history = get_git_log()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        summary_data = {
            "timestamp": timestamp,
            "version": "1.0.0",
            "git_log": git_history,
            "description": "Release summary generated automatically by TOAI ecosystem."
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
