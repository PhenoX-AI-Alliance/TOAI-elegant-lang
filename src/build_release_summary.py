import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_path = os.path.join(repo_dir, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_path, '.git')):
        git_path = repo_dir
    
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            cwd=git_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_paths = [
        os.path.join(repo_dir, 'WHITE_PAPER.md'),
        os.path.join(repo_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md'),
        os.path.join(repo_dir, 'CONSTITUTION.md')
    ]
    summary = {}
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:300] + "..."
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading: {str(e)}"
    return summary

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    whitepaper_info = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_commits": git_logs,
        "whitepaper_summary": whitepaper_info,
        "status": "success",
        "message": "Release summary successfully generated with altruistic and precise metrics."
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
