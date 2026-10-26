import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_command(cmd, cwd):
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
    except Exception as e:
        print(f"Git command failed {{cmd}}: {{e}}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository not found at target path. Initializing...", file=sys.stderr)
        os.makedirs(repo_dir, exist_ok=True)
        subprocess.run(['git', 'init'], cwd=repo_dir, check=True)
        subprocess.run(['git', 'config', 'user.name', 'TOAI Builder'], cwd=repo_dir, check=True)
        subprocess.run(['git', 'config', 'user.email', 'builder@toai.local'], cwd=repo_dir, check=True)
        # Create initial commit if empty
        with open(os.path.join(repo_dir, 'README.md'), 'w') as f:
            f.write("# TOAI Elegant Lang\n")
        subprocess.run(['git', 'add', 'README.md'], cwd=repo_dir, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=repo_dir, check=True)

    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    latest_tag = run_git_command(['git', 'describe', '--tags', '--abbrev=0'], repo_dir)
    if not latest_tag:
        latest_tag = "v0.1.0"

    whitepaper_path = os.path.join(repo_dir, 'WHITE_PAPER.md')
    whitepaper_summary = "No whitepaper found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            whitepaper_summary = "".join(lines[:15])

    release_data = {
        "version": latest_tag,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "git_log": git_log.splitlines(),
        "whitepaper_excerpt": whitepaper_summary
    }

    output_path = os.path.join(repo_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated release summary at {{output_path}}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
