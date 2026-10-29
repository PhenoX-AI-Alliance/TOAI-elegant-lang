import sys
import os
import subprocess
import json
import traceback
from datetime import datetime

def main():
    try:
        repo_dir = os.getcwd()
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            # Try parent directory
            parent = os.path.dirname(repo_dir)
            if os.path.exists(os.path.join(parent, '.git')):
                repo_dir = parent
            else:
                print("Error: Not a git repository.")
                sys.exit(1)

        print(f"Scanning git log in {repo_dir}...")
        res = subprocess.run(
            ['git', '-C', repo_dir, 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        git_logs = res.stdout.strip().split('\n')

        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "recent_commits": git_logs,
            "ecosystem": "Gaia Ecosystem - Earth of Life"
        }

        output_path = os.path.join(repo_dir, 'TOAI-elegant-lang', 'release_summary.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)

        print(f"Successfully generated release summary at {output_path}")

    except Exception as e:
        print(f"Error during release summary generation: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
