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
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("Git repository not found. Initializing...")
        try:
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Builder'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'builder@toai.internal'], cwd=repo_path, check=True)
        except Exception as e:
            print(f"Failed to initialize git repository: {e}")
            sys.exit(1)

    git_log = run_git_command(['log', '-n', '10', '--oneline'], repo_path)
    git_status = run_git_command(['status', '--short'], repo_path)
    
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:500]

    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_log": git_log,
        "git_status": git_status,
        "whitepaper_excerpt": whitepaper_content
    }

    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Release summary successfully generated at {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
