import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr.strip()}")
        return None
    except Exception as e:
        print(f"Unexpected error running command {' '.join(cmd)}: {e}")
        return None

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}")
        sys.exit(1)
        
    git_check = run_command(['git', 'rev-parse', '--is-inside-work-tree'], cwd=repo_dir)
    if not git_check or git_check != 'true':
        print("Target directory is not a valid git repository. Initializing...")
        run_command(['git', 'init'], cwd=repo_dir)
        run_command(['git', 'config', 'user.name', 'TOAI Release Agent'], cwd=repo_dir)
        run_command(['git', 'config', 'user.email', 'agent@toai.local'], cwd=repo_dir)
        run_command(['git', 'add', '.'], cwd=repo_dir)
        run_command(['git', 'commit', '-m', 'Initial commit by TOAI release agent'], cwd=repo_dir)

    git_log = run_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar: %s'], cwd=repo_dir)
    if git_log is None:
        git_log = "No commit history available."

    whitepaper_path = os.path.join(repo_dir, 'WHITESPAPER.md')
    whitepaper_content = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:2000]
        except Exception as e:
            whitepaper_content = f"Failed to read whitepaper: {e}"

    summary_data = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "recent_commits": git_log.splitlines(),
        "whitepaper_excerpt": whitepaper_content
    }

    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        print(f"Failed to write release summary json: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
