import sys
import os
import traceback
import subprocess
import json
import datetime

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        git_log = ""
        if os.path.exists(os.path.join(repo_path, '.git')):
            try:
                result = subprocess.run(
                    ['git', '-C', repo_path, 'log', '-n', '10', '--pretty=format:%h - %an, %ad : %s'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                git_log = result.stdout
            except Exception as e:
                git_log = f"Failed to fetch git log: {str(e)}"
        else:
            git_log = "Not a git repository or git not initialized."

        whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
        whitepaper_summary = "Whitepaper not found."
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                whitepaper_summary = "".join(lines[:20])

        release_info = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_log,
            "whitepaper_excerpt": whitepaper_summary
        }

        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=4)

        print(f"Release summary successfully generated at: {output_file}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
