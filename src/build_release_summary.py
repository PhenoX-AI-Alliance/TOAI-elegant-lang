import sys
import os
import traceback
import time
import json
import subprocess
import datetime

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
        print(f"Warning: Failed to fetch git log: {{e}}", file=sys.stderr)
        return []

def scan_whitepaper(repo_path):
    whitepaper_candidates = ['WHITEPAPER.md', 'README.md', 'CONSTITUTION.md']
    summary_info = {}
    for candidate in whitepaper_candidates:
        full_path = os.path.join(repo_path, candidate)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    first_lines = [line.strip() for line in content.split('\n') if line.strip()][:5]
                    summary_info[candidate] = first_lines
            except Exception as e:
                print(f"Warning: Failed to read {{candidate}}: {{e}}", file=sys.stderr)
    return summary_info

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {{repo_path}}", file=sys.stderr)
        sys.exit(1)
    
    git_logs = get_git_log(repo_path)
    whitepaper_info = scan_whitepaper(repo_path)
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_commits": git_logs,
        "documents": whitepaper_info,
        "status": "success"
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {{output_path}}")
    except Exception as e:
        print(f"Error: Failed to write release summary json: {{e}}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n