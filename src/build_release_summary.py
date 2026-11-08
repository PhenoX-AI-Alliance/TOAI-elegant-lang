import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

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
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e.stderr.strip()}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"Unexpected error running git command: {str(e)}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Repository path does not exist: {repo_path}", file=sys.stderr)
        sys.exit(1)
        
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        print(f"Not a git repository (missing .git): {repo_path}", file=sys.stderr)
        sys.exit(1)
        
    print("Fetching git log...")
    git_log = run_git_command(['git', 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'], repo_path)
    
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        print("Reading whitepaper...")
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:2000]
        except Exception as e:
            print(f"Failed to read whitepaper: {str(e)}", file=sys.stderr)
            
    summary_data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "git_log": git_log.splitlines() if git_log else [],
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Release summary successfully written to {output_file}")
    except Exception as e:
        print(f"Failed to write release summary json: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
