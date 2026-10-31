import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_candidates = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'CONSTITUTION.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'README.md')
    ]
    summary = {}
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading file: {str(e)}"
    return summary

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    whitepaper_data = scan_whitepaper(workspace_dir)
    
    release_summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_recent_commits": git_logs,
        "whitepaper_snippets": whitepaper_data,
        "status": "success"
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n