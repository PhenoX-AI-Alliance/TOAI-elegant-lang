import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        TOAI_elegant_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(TOAI_elegant_dir, '.git')):
            return "Git repository not found in target path."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=TOAI_elegant_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        TOAI_elegant_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
        whitepaper_path = os.path.join(TOAI_elegant_dir, 'WHITEPAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:30])
        return "Whitepaper not found."
    except Exception as e:
        return f"Failed to read whitepaper: {str(e)}"

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_log = get_git_log()
        whitepaper_snippet = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_log,
            "whitepaper_snippet": whitepaper_snippet
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built and saved to {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
