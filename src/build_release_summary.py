import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_command(cmd, cwd):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Git command failed {{cmd}}: {{e}}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository not found. Initializing repository for release tracking...")
        try:
            os.makedirs(repo_dir, exist_ok=True)
            subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Executor'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.email', 'executor@toai.internal'], cwd=repo_dir, check=True)
        except Exception as init_err:
            print(f"Failed to initialize git repository: {{init_err}}")
    
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    if not git_log:
        git_log = "No commit history available yet."
        
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_content = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:2000]
        except Exception as wp_err:
            whitepaper_content = f"Error reading whitepaper: {{wp_err}}"
            
    summary = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0-gaia",
        "git_recent_logs": git_log.splitlines(),
        "whitepaper_excerpt": whitepaper_content[:500]
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as out_f:
        json.dump(summary, out_f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated release summary at {{output_path}}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
