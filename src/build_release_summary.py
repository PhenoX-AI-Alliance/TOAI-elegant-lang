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
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_dir = os.path.join(workspace, 'TOAI-elegant-lang')
        
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            print("Git repository not found. Initializing release summary based on file scan.")
            git_log = "No git repository found."
        else:
            git_log = run_git_command(['log', '-n', '10', '--oneline'], repo_dir)
            
        whitepaper_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
        whitepaper_content = ""
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:1000]
                
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_logs": git_log,
            "whitepaper_excerpt": whitepaper_content,
            "version": "1.0.0-alpha"
        }
        
        output_path = os.path.join(workspace, 'TOAI-Generated', 'release_summary.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully built at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
