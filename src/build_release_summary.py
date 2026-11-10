import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_paths = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
    ]
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                return "".join(lines[:20])
            except Exception:
                pass
    return "Whitepaper not found or unreadable."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_commits = get_git_log()
    whitepaper_snippet = scan_whitepaper(workspace_dir)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_commits,
        "whitepaper_overview": whitepaper_snippet
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
