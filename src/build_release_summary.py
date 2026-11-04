import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper(repo_path):
    candidates = ['WHITEPAPER.md', 'README.md', 'CONSTITUTION.md']
    summary_data = {}
    for filename in candidates:
        filepath = os.path.join(repo_path, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    summary_data[filename] = [line.strip() for line in lines[:15] if line.strip()]
            except Exception as e:
                print(f"Warning: Could not read {filename}: {e}")
    return summary_data

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_logs = get_git_log(repo_path)
    whitepaper_info = scan_whitepaper(repo_path)
    
    release_data = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "git_history": git_logs,
        "whitepaper_snippets": whitepaper_info
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
