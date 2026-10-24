import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

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
        print(e.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        print("Git repository not initialized in target directory. Initializing...")
        os.makedirs(repo_dir, exist_ok=True)
        run_command(['git', 'init'], cwd=repo_dir)
        run_command(['git', 'config', 'user.name', 'TOAI Executor'], cwd=repo_dir)
        run_command(['git', 'config', 'user.email', 'executor@toai.local'], cwd=repo_dir)
        # Create an initial commit if empty
        readme_path = os.path.join(repo_dir, 'README.md')
        if not os.path.exists(readme_path):
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write("# TOAI-elegant-lang\nInitial release.")
            run_command(['git', 'add', 'README.md'], cwd=repo_dir)
            run_command(['git', 'commit', '-m', 'Initial commit'], cwd=repo_dir)

    git_log = run_command(['git', 'log', '-n', '10', '--oneline'], cwd=repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_content = "No whitepaper found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:500]

    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_log": git_log.splitlines(),
        "whitepaper_excerpt": whitepaper_content
    }

    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
