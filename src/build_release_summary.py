import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper(repo_path):
    whitepaper_paths = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'src', 'WHITEPAPER.md')
    ]
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000] # Return first 1000 chars as summary
            except Exception as e:
                print(f"Warning: Could not read whitepaper at {path}: {e}")
    return "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("Scanning repository for release summary...")
    
    git_logs = get_git_log(repo_path)
    whitepaper_summary = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": git_logs,
        "whitepaper_excerpt": whitepaper_summary
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
