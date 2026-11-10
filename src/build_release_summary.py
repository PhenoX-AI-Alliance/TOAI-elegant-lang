import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_logs():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git logs: {str(e)}"]

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_dir = os.path.join(workspace, 'TOAI-elegant-lang')
    whitepapers = []
    if os.path.exists(target_dir):
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    whitepapers.append(os.path.join(root, file))
    return whitepapers

def main():
    print("Building release summary...")
    logs = get_git_logs()
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": logs,
        "related_documents": papers
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    main()
