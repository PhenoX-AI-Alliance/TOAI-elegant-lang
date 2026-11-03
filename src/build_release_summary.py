import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}", file=sys.stderr)
        return []

def scan_whitepaper(repo_path):
    papers = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if 'whitepaper' in file.lower() or 'summary' in file.lower() or file.endswith('.md'):
                papers.append(os.path.join(root, file))
    return papers

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_commits = get_git_log(repo_path)
    whitepapers = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "recent_commits": git_commits,
        "related_documents": whitepapers[:10]
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
