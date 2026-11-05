import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_command(args, cwd):
    try:
        res = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return f"Error executing git command: {e}"

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_dir):
            print(f"Repository directory not found: {repo_dir}")
            sys.exit(1)
            
        git_check = os.path.join(repo_dir, '.git')
        if not os.path.exists(git_check):
            print("Git repository not initialized. Initializing for release summary...")
            subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Release Agent'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.email', 'agent@toai.internal'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True)
            try:
                subprocess.run(['git', 'commit', '-m', 'Initial commit for release summary'], cwd=repo_dir, check=True)
            except Exception:
                pass

        commit_log = run_git_command(['log', '-n', '10', '--oneline'], repo_dir)
        
        whitepaper_path = os.path.join(repo_dir, 'WHITE_PAPER.md')
        whitepaper_summary = "Whitepaper not found."
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                whitepaper_summary = "".join(lines[:20])
                
        release_info = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": commit_log,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
