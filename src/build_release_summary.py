import sys
import os
import subprocess
import json
from datetime import datetime

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print("[*] Scanning git log and whitepapers...")
    git_logs = "No git repository found or error executing git."
    if os.path.exists(os.path.join(repo_path, '.git')):
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_logs = result.stdout
        except Exception as e:
            git_logs = f"Git log error: {str(e)}"
    else:
        try:
            result = subprocess.run(
                ['git', 'log', '-n', '10', '--oneline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_logs = result.stdout
        except Exception as e:
            git_logs = f"Fallback git log error: {str(e)}"

    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "git_recent_commits": git_logs.splitlines(),
        "ecosystem": "Gaia Ecosystem - Earth of Life"
    }

    output_file = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"[+] Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(f"[-] Error in build_release_summary: {err}", file=sys.stderr)
        sys.exit(1)
