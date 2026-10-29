import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_command(args, cwd):
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Git command failed: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository not found. Initializing repository...")
        try:
            subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Executor'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.email', 'executor@toai.local'], cwd=repo_dir, check=True)
        except Exception as e:
            print(f"Failed to initialize git repo: {e}")
            sys.exit(1)

    log_output = run_git_command(['log', '-n', '10', '--oneline'], cwd=repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITESPAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:500]
            
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": log_output.splitlines() if log_output else [],
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
