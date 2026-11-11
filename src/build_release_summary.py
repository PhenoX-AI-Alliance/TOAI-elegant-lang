import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_workspace():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    files_found = []
    if os.path.exists(target_path):
        for root, dirs, files in os.walk(target_path):
            for file in files:
                files_found.append(os.path.relpath(os.path.join(root, file), workspace_dir))
    return files_found

def main():
    print("Generating release summary...")
    logs = get_git_log()
    files = scan_workspace()
    
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_recent_commits": logs,
        "tracked_files_count": len(files),
        "tracked_files": files[:50]
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully written to {output_file}")

if __name__ == '__main__':
    main()
