import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepapers(repo_path):
    papers = []
    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        pass
    return papers

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            subprocess.run(['git', 'init', repo_path], capture_output=True)
            
        logs = get_git_log(repo_path)
        whitepapers = scan_whitepapers(repo_path)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "repository": "TOAI-elegant-lang",
            "git_logs": logs,
            "whitepapers_found": whitepapers
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
