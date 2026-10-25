import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not initialized."
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper(workspace_path):
    whitepaper_files = []
    for root, dirs, files in os.walk(workspace_path):
        for file in files:
            if 'whitepaper' in file.lower() or 'release' in file.lower() or file.endswith('.md'):
                whitepaper_files.append(os.path.join(root, file))
    return whitepaper_files

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print("Scanning Git log...")
    git_logs = get_git_log(repo_path)
    
    print("Scanning documentation and whitepapers...")
    docs = scan_whitepaper(workspace)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": git_logs,
        "related_documents": docs[:10]
    }
    
    output_json_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at {output_json_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
