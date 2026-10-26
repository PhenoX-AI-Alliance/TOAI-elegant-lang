import sys
import os
import subprocess
import json
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return ''.join(lines[:30])
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_commits = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    release_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_commits,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at {output_path}")

if __name__ == '__main__':
    main()
