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
        
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            print(f"Error: {repo_dir} is not a valid git repository.")
            sys.exit(1)
            
        print("Scanning git log...")
        git_log = run_git_command(['log', '-n', '20', '--oneline'], repo_dir)
        
        whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
        whitepaper_content = ""
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()
        else:
            whitepaper_content = "Whitepaper not found."
            
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "git_log": git_log.splitlines() if git_log else [],
            "whitepaper_snippet": whitepaper_content[:500] if whitepaper_content else ""
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
