import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

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
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(args)}, error: {e.stderr.strip()}")
        return ""
    except Exception as e:
        print(f"Unexpected error running git: {e}")
        return ""

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_dir):
            print(f"Repository directory not found: {repo_dir}")
            sys.exit(1)
            
        git_check = run_git_command(['rev-parse', '--is-inside-work-tree'], repo_dir)
        if git_check != 'true':
            print("Target directory is not a git repository.")
            sys.exit(1)
            
        commit_log = run_git_command(['log', '-n', '20', '--pretty=format:%h - %an, %ad : %s'], repo_dir)
        
        whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
        whitepaper_content = ""
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()
        else:
            whitepaper_content = "Whitepaper not found."
            
        release_summary = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "recent_commits": commit_log.splitlines() if commit_log else [],
            "whitepaper_summary": whitepaper_content[:500] + "..." if len(whitepaper_content) > 500 else whitepaper_content
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
