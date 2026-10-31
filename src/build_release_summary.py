import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        target_repo = os.path.join(repo_path, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(target_repo, '.git')):
            return "Git repository not found or not initialized."
        
        result = subprocess.run(
            ['git', '-C', target_repo, 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def scan_whitepaper():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        whitepaper_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content[:500] + "... [truncated]"
        return "Whitepaper not found."
    except Exception as e:
        return f"Could not read whitepaper: {str(e)}"

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_log = get_git_log()
        whitepaper_snippet = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "git_log": git_log,
            "whitepaper_snippet": whitepaper_snippet,
            "status": "success"
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
