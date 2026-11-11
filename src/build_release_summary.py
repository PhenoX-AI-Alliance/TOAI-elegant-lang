import os
import sys
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=20):
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(git_dir):
        git_dir = repo_path
    
    try:
        cmd = ['git', '-C', git_dir, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_files = ['README.md', 'CONSTITUTION.md', 'WHITE_PAPER.md']
    summary_data = {}
    
    for filename in target_files:
        path = os.path.join(repo_path, filename)
        if not os.path.exists(path):
            path = os.path.join(repo_path, 'TOAI-elegant-lang', filename)
            
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary_data[filename] = content[:500] + ('...' if len(content) > 500 else '')
            except Exception as e:
                summary_data[filename] = f"Error reading file: {str(e)}"
        else:
            summary_data[filename] = "File not found."
            
    return summary_data

def generate_release_summary():
    logs = get_git_log(30)
    whitepaper = scan_whitepaper()
    
    release_info = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_recent_commits": logs,
        "whitepaper_snippets": whitepaper
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    generate_release_summary()
