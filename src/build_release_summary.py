import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(max_count=20):
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not found."
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper():
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    potential_paths = [
        os.path.join(repo_path, 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'CONSTITUTION.md')
    ]
    for path in potential_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000]
            except Exception:
                pass
    return "No whitepaper found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_log = get_git_log()
        whitepaper_snippet = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_log,
            "whitepaper_snippet": whitepaper_snippet
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
