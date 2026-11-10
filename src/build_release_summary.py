import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            
        git_dir = os.path.join(repo_path, '.git')
        git_logs = "No git repository found or no commits yet."
        if os.path.exists(git_dir):
            try:
                result = subprocess.run(
                    ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                git_logs = result.stdout
            except Exception as e:
                git_logs = f"Failed to fetch git log: {str(e)}"
        else:
            try:
                subprocess.run(['git', '-C', repo_path, 'init'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(['git', '-C', repo_path, 'config', 'user.name', 'TOAI Executor'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(['git', '-C', repo_path, 'config', 'user.email', 'executor@toai.internal'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                with open(os.path.join(repo_path, 'README.md'), 'w') as f:
                    f.write("# TOAI-elegant-lang\nInitialized by TOAI Release Summary Script.\n")
                subprocess.run(['git', '-C', repo_path, 'add', 'README.md'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                subprocess.run(['git', '-C', repo_path, 'commit', '-m', 'Initial commit'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                result = subprocess.run(
                    ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                git_logs = result.stdout
            except Exception as init_err:
                git_logs = f"Git init and log fallback failed: {str(init_err)}"

        summary_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "repository": "TOAI-elegant-lang",
            "git_recent_logs": git_logs.splitlines(),
            "status": "success",
            "message": "Release summary successfully generated from repository state."
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
