import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not found. Skipping git log."
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Failed to fetch git log: {e}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content[:500] + "... [truncated]"
        except Exception as e:
            return f"Error reading whitepaper: {e}"
    return "WHITEPAPER.md not found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_history = run_git_log()
        whitepaper_summary = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "git_log": git_history,
            "whitepaper_summary": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
