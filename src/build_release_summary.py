import sys
import os
import traceback
import subprocess
import json
import datetime

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        git_log = ""
        if os.path.exists(os.path.join(repo_path, '.git')):
            try:
                result = subprocess.run(
                    ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                git_log = result.stdout
            except Exception as e:
                git_log = f"Could not fetch git log: {e}"
        else:
            git_log = "Git repository not initialized at target path."
            
        whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
        whitepaper_summary = "Whitepaper not found."
        if os.path.exists(whitepaper_path):
            try:
                with open(whitepaper_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    whitepaper_summary = "".join(lines[:20])
            except Exception as e:
                whitepaper_summary = f"Could not read whitepaper: {e}"
                
        release_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_log.splitlines(),
            "whitepaper_excerpt": whitepaper_summary
        }
        
        output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
