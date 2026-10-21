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
        print(f"Git command failed {{cmd}}: {{e}}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("Git repository not found. Initializing repository for release summary...")
        try:
            subprocess.run(["git", "init"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.name", "TOAI Release Bot"], cwd=repo_path, check=True)
            subprocess.run(["git", "config", "user.email", "bot@toai.local"], cwd=repo_path, check=True)
        except Exception as init_err:
            print(f"Failed to initialize git repository: {{init_err}}")
            sys.exit(1)
            
    # Stage and commit if needed to ensure git log works
    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", "chore: auto sync before release summary"], cwd=repo_path, check=True)
    except Exception:
        pass # Nothing to commit or already committed
        
    git_log = run_git_command(["git", "log", "-n", "10", "--pretty=format:%h - %an: %s (%ar)"], repo_path)
    if not git_log:
        git_log = "No commit history available yet."
        
    whitepaper_path = os.path.join(workspace_dir, 'TOAI_Generated', 'WHITEPAPER.md')
    whitepaper_summary = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                whitepaper_summary = content[:1000] + ("..." if len(content) > 1000 else "")
        except Exception as e:
            whitepaper_summary = f"Error reading whitepaper: {{e}}"
            
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "git_recent_commits": git_log.splitlines(),
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {{output_path}}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
