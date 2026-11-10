import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_logs(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepapers(workspace_path):
    papers = []
    for root, dirs, files in os.walk(workspace_path):
        for file in files:
            if 'whitepaper' in file.lower() or file.endswith('.md'):
                papers.append(os.path.join(root, file))
    return papers

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        git_logs = get_git_logs(repo_path)
        whitepapers = scan_whitepapers(workspace)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "repository": repo_path,
            "recent_commits": git_logs,
            "discovered_documents": whitepapers[:10]
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully generated release summary at {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
