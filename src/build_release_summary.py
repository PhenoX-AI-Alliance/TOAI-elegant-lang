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
        print(f"Git command failed: {e}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}", file=sys.stderr)
        sys.exit(1)
        
    git_check = run_git_command(['rev-parse', '--is-inside-work-tree'], repo_dir)
    if git_check != 'true':
        print(f"Directory is not a git repository: {repo_dir}", file=sys.stderr)
        sys.exit(1)
        
    log_output = run_git_command(['log', '-n', '10', '--oneline'], repo_dir)
    latest_tag = run_git_command(['describe', '--tags', '--abbrev=0'], repo_dir) or "v0.1.0"
    
    summary_data = {
        "timestamp": datetime.datetime.utcnow().isoformat() + " Z",
        "latest_tag": latest_tag,
        "recent_commits": log_output.splitlines() if log_output else []
    }
    
    output_file = os.path.join(repo_dir, 'release_summary.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        print(f"Failed to write release summary file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
