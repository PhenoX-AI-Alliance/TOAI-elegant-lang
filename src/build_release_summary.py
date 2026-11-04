import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_log(repo_path):
    try:
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return "Git repository not initialized."
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to fetch git log: {str(e)}"

def scan_whitepapers(workspace_path):
    whitepapers = []
    try:
        for root, dirs, files in os.walk(workspace_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    whitepapers.append(full_path)
    except Exception as e:
        print(f"Error scanning whitepapers: {e}", file=sys.stderr)
    return whitepapers

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("Scanning repository and whitepapers for release summary...")
    git_logs = run_git_log(repo_path)
    whitepapers = scan_whitepapers(workspace_dir)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepapers_found": whitepapers[:20]
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n