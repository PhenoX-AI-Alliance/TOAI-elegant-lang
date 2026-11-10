import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        git_log = "No git history available."
        if os.path.exists(os.path.join(repo_path, '.git')):
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0:
                git_log = result.stdout
        
        whitepaper_path = os.path.join(workspace_dir, 'WHITE_PAPER.md')
        whitepaper_summary = "Whitepaper not found."
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                whitepaper_summary = "".join(lines[:20])
                
        release_info = {
            "timestamp": datetime.now().isoformat(),
            "git_recent_commits": git_log.splitlines(),
            "whitepaper_excerpt": whitepaper_summary
        }
        
        output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
