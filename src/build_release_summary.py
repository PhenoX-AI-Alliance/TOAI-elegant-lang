import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs(repo_path):
    logs = []
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '-n', '10', '--pretty=format:%h - %an, %ad : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        logs = result.stdout.splitlines()
    except Exception as e:
        logs = [f"Could not fetch git logs: {str(e)}"]
    return logs

def scan_whitepaper(workspace_path):
    content = ""
    wp_path = os.path.join(workspace_path, 'WHITE_PAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()[:1000]
        except Exception as e:
            content = f"Error reading WHITE_PAPER.md: {str(e)}"
    else:
        content = "WHITE_PAPER.md not found."
    return content

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("Scanning repository and whitepaper for release summary...")
    logs = get_git_logs(repo_path)
    whitepaper_snippet = scan_whitepaper(workspace_dir)
    
    summary = {
        "generated_at": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepaper_overview": whitepaper_snippet
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
