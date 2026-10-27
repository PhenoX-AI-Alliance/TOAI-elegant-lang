import sys
import os
import subprocess
import json
import glob
from datetime import datetime

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    git_logs = []
    if os.path.exists(os.path.join(repo_path, '.git')):
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_logs = result.stdout.strip().split('\n')
        except Exception as e:
            git_logs = [f"Error fetching git log: {str(e)}"]
    else:
        git_logs = ["Git repository not initialized or not found."]
        
    whitepapers = []
    wp_pattern = os.path.join(workspace, '**', '*.md')
    for file_path in glob.glob(wp_pattern, recursive=True):
        if 'TOAI_Generated' not in file_path:
            whitepapers.append(file_path)
            
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_recent_commits": git_logs,
        "scanned_documents": whitepapers[:20]
    }
    
    output_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in build_release_summary: {e}", file=sys.stderr)
        sys.exit(1)