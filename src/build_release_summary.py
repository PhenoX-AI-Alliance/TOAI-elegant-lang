import sys
import os
import traceback
import time
import json
import subprocess

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace_dir):
    candidates = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    summary = {}
    for c in candidates:
        path = os.path.join(workspace_dir, 'TOAI-elegant-lang', c)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    summary[c] = f.readline().strip()
            except Exception as e:
                summary[c] = f"Error reading file: {str(e)}"
    return summary

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    whitepaper_info = scan_whitepaper(workspace_dir)
    
    release_data = {
        "timestamp": time.time(),
        "git_recent_commits": git_logs,
        "documentation_summary": whitepaper_info,
        "version": "1.0.0-alpha"
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
