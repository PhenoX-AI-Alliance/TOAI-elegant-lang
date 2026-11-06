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
            return "No git repository found in TOAI-elegant-lang."
        
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
        return f"Could not retrieve git log: {e}"

def scan_whitepaper():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        whitepaper_path = os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:30])
        return "Whitepaper not found."
    except Exception as e:
        return f"Could not read whitepaper: {e}"

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_log_data = get_git_log()
        whitepaper_data = scan_whitepaper()
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        summary = {
            "timestamp": timestamp,
            "version_summary": "TOAI Elegant Lang Release Summary",
            "git_log": git_log_data,
            "whitepaper_excerpt": whitepaper_data
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
