import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def run_git_command(repo_path):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper(repo_path):
    whitepaper_path = os.path.join(repo_path, 'WHITE_PAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                return "\n".join(lines[:20])
        except Exception as e:
            return f"Error reading WHITE_PAPER.md: {str(e)}"
    return "WHITE_PAPER.md not found."

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        git_log = "Git repository not initialized."
        if os.path.exists(os.path.join(repo_path, '.git')):
            git_log = run_git_command(repo_path)
        
        whitepaper_summary = scan_whitepaper(repo_path)
        
        release_info = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_log,
            "whitepaper_summary": whitepaper_summary
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
