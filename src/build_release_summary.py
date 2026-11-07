import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            try:
                subprocess.run(['git', 'init', repo_path], check=True)
            except Exception:
                pass

        git_commits = get_git_log(repo_path)
        
        whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
        whitepaper_summary = "Whitepaper not found."
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                whitepaper_summary = "".join(lines[:10])

        release_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "recent_commits": git_commits,
            "whitepaper_excerpt": whitepaper_summary
        }

        output_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)

        print(f"Successfully generated release summary at {output_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
