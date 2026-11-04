import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=10):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not initialized."
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper(workspace_path):
    whitepaper_files = []
    for root, dirs, files in os.walk(workspace_path):
        for file in files:
            if 'whitepaper' in file.lower() or 'doc' in file.lower() or 'release' in file.lower():
                whitepaper_files.append(os.path.join(root, file))
    return whitepaper_files

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print("Scanning git logs and documentation...")
    git_history = get_git_log(repo_path)
    docs = scan_whitepaper(workspace)
    
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_log": git_history,
        "related_documents": docs[:10]
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n