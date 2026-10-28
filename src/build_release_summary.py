import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'))
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'TOAI-elegant-lang', 'WHITE_PAPER.md'),
        os.path.join(workspace, 'docs', 'WHITE_PAPER.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.splitlines()
                    for line in lines:
                        if 'version' in line.lower() or 'release' in line.lower():
                            return line.strip()
            except Exception as e:
                print(f"Warning: Could not read whitepaper at {path}: {e}")
    return "Version info not found in whitepaper."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    print("Scanning repository and whitepaper for release summary...")
    git_commits = get_git_log(15)
    whitepaper_info = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "whitepaper_summary": whitepaper_info,
        "recent_commits": git_commits
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built and saved to {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
