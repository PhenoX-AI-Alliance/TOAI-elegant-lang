import sys
import os
import traceback
import json
import subprocess
from datetime import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    git_log = "No git history available."
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
            git_log = f"Failed to fetch git log: {str(e)}"
    
    whitepaper_path = os.path.join(workspace_dir, 'TOAI_Generated', 'whitepaper.md')
    whitepaper_summary = "No whitepaper found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                whitepaper_summary = content[:500] + "..." if len(content) > 500 else content
        except Exception as e:
            whitepaper_summary = f"Failed to read whitepaper: {str(e)}"
            
    release_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_log": git_log,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
