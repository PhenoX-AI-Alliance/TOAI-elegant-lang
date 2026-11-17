import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        pass
    return whitepaper_files

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Repository path does not exist: {repo_path}")
        sys.exit(1)
        
    git_logs = get_git_log(repo_path)
    whitepapers = scan_whitepaper(repo_path)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "repository": repo_path,
        "recent_commits": git_logs,
        "documentation_files": whitepapers
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
