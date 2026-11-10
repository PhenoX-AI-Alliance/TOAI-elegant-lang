import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("[INFO] Starting release summary generation...")
    
    git_log = ""
    try:
        if os.path.exists(os.path.join(repo_dir, '.git')):
            result = subprocess.run(
                ['git', 'log', '-n', '10', '--oneline'],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=True
            )
            git_log = result.stdout
        else:
            git_log = "Git repository not initialized or not found."
    except Exception as e:
        git_log = f"Failed to retrieve git log: {str(e)}"
        
    whitepaper_content = "No whitepaper found."
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:1000] # Read first 1000 chars as summary
        except Exception as e:
            whitepaper_content = f"Failed to read whitepaper: {str(e)}"
            
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": git_log.splitlines(),
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"[SUCCESS] Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
