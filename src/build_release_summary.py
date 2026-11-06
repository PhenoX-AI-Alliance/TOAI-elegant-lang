import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def run_git_command(args):
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.isdir(git_dir):
        git_dir = repo_path
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=git_dir,
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
    target_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'src')
    os.makedirs(target_dir, exist_ok=True)
    
    output_path = os.path.join(target_dir, 'release_summary.json')
    
    git_log = run_git_command(['log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'])
    git_status = run_git_command(['status', '--short'])
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_log.splitlines() if git_log else [],
        "git_status": git_status.splitlines() if git_status else [],
        "version": "1.0.0",
        "ecosystem": "Gaia Ecosystem - TOAI"
    }
    
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
