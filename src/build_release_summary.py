import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--oneline']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepapers(base_dir):
    whitepapers = []
    try:
        for root, dirs, files in os.walk(base_dir):
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
        
        print("Scanning repository and generating release summary...")
        
        git_commits = get_git_log(repo_path)
        whitepapers = scan_whitepapers(repo_path)
        
        summary_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "git_recent_commits": git_commits,
            "detected_whitepapers": whitepapers,
            "status": "success"
        }
        
        output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
