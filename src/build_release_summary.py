import sys
import os
import traceback
import subprocess
import json
import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("[INFO] Starting release summary generation...")
    
    git_log = "No git repository found or git command failed."
    if os.path.exists(os.path.join(repo_path, '.git')):
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_log = result.stdout
        except Exception as e:
            git_log = f"Failed to retrieve git log: {str(e)}"
    else:
        print("[WARN] Not a git repository, skipping git log collection.")

    whitepaper_content = "Whitepaper not found."
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:1000]
        except Exception as e:
            whitepaper_content = f"Failed to read whitepaper: {str(e)}"

    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": git_log,
        "whitepaper_excerpt": whitepaper_content
    }

    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"[SUCCESS] Release summary successfully written to {output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to write release summary: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
