import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_log():
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not found."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Git error: {e.stderr}"
    except Exception as e:
        return f"Unexpected error running git: {str(e)}"

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md'),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'WHITE_PAPER.md'))
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:2000] # Return first 2000 chars as summary
            except Exception as e:
                return f"Error reading whitepaper at {path}: {str(e)}"
    return "Whitepaper not found."

def main():
    try:
        git_logs = run_git_log()
        whitepaper_summary = scan_whitepaper()
        
        release_info = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "git_recent_commits": git_logs,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at {output_path}")
    except Exception as e:
        print(f"Error in release summary builder: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
