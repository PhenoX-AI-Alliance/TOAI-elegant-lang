import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        git_log = "No git history available."
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
        else:
            try:
                subprocess.run(['git', '-C', repo_dir, 'init'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(['git', '-C', repo_dir, 'config', 'user.name', 'TOAI Builder'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(['git', '-C', repo_dir, 'config', 'user.email', 'builder@toai.internal'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(['git', '-C', repo_dir, 'add', '.'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(['git', '-C', repo_dir, 'commit', '-m', 'Initial commit by TOAI builder', '--allow-empty'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                result = subprocess.run(
                    ['git', '-C', repo_dir, 'log', '-n', '10', '--oneline'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                git_log = result.stdout
            except Exception as inner_e:
                git_log = f"Git initialization and log fallback failed: {str(e)}"

        whitepaper_content = "Whitepaper not found."
        whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:2000]

        summary_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "git_log": git_log,
            "whitepaper_excerpt": whitepaper_content
        }

        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
