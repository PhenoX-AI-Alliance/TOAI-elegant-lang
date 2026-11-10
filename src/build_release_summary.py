import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_candidates = ['WHITEPAPER.md', 'README.md', 'CONSTITUTION.md']
    summary = {}
    for filename in whitepaper_candidates:
        file_path = os.path.join(repo_path, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[filename] = content[:500] + ('...' if len(content) > 500 else '')
            except Exception as e:
                summary[filename] = f"Error reading file: {str(e)}"
    return summary

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        os.makedirs(repo_path, exist_ok=True)
        try:
            subprocess.run(['git', 'init', repo_path], check=True)
        except Exception:
            pass

    git_logs = get_git_log(repo_path)
    whitepaper_data = scan_whitepaper(repo_path)
    
    release_info = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "git_recent_commits": git_logs,
        "whitepaper_summary": whitepaper_data
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
