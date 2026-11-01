import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers(workspace_path):
    papers = []
    try:
        for root, dirs, files in os.walk(workspace_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error scanning files: {e}", file=sys.stderr)
    return papers

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        
    git_commits = get_git_log(repo_path)
    whitepapers = scan_whitepapers(workspace_dir)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "repository": repo_path,
        "recent_commits": git_commits,
        "discovered_documents": whitepapers[:10]
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n