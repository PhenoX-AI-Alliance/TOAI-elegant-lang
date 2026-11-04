import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print(f"Initializing git repository at {repo_path}")
            os.makedirs(repo_path, exist_ok=True)
            subprocess.run(['git', 'init', repo_path], check=True)
            
        logs = get_git_log(repo_path)
        
        whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITESPAPER.md')
        whitepaper_content = "Whitepaper not found."
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:500] # preview
                
        summary = {
            "timestamp": datetime.now().isoformat(),
            "git_logs": logs,
            "whitepaper_preview": whitepaper_content
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
