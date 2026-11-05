import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git logs: {e}")
        return []

def scan_whitepapers(repo_path):
    whitepapers = []
    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    whitepapers.append(full_path)
    except Exception as e:
        print(f"Warning: Could not scan whitepapers: {e}")
    return whitepapers

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        print(f"Scanning repository at: {repo_path}")
        
        logs = []
        if os.path.exists(os.path.join(repo_path, '.git')):
            logs = get_git_logs(repo_path)
        else:
            print("Notice: .git directory not found in TOAI-elegant-lang. Skipping git log retrieval.")
            
        whitepapers = scan_whitepapers(repo_path)
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "repository": "TOAI-elegant-lang",
            "git_logs": logs,
            "whitepapers_found": whitepapers
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
