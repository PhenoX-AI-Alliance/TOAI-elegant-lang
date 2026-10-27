import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_command(cmd, cwd):
    try:
        res = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        print(f"Git command failed: {cmd}, Error: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository not found. Initializing...")
        try:
            os.makedirs(repo_dir, exist_ok=True)
            subprocess.run(["git", "init"], cwd=repo_dir, check=True)
        except Exception as e:
            print(f"Failed to initialize git repository: {e}")
    
    git_log = run_git_command(["git", "log", "-n", "10", "--oneline"], repo_dir)
    if not git_log:
        git_log = "No commit history available."
        
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_content = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:2000]
        except Exception as e:
            whitepaper_content = f"Error reading whitepaper: {e}"
            
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_log": git_log,
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_path = os.path.join(repo_dir, 'src', 'release_summary.json')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {output_path}")
    except Exception as e:
        print(f"Failed to write release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
