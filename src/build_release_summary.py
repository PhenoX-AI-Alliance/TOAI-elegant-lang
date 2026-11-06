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
        print(e.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Repository directory not found: {repo_dir}")
        sys.exit(1)
        
    git_dir = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_dir):
        print("Not a git repository. Initializing git...")
        run_command(['git', 'init'], cwd=repo_dir)
        run_command(['git', 'config', 'user.name', 'TOAI Release Agent'], cwd=repo_dir)
        run_command(['git', 'config', 'user.email', 'agent@toai.ecosystem'], cwd=repo_dir)
        run_command(['git', 'add', '.'], cwd=repo_dir)
        run_command(['git', 'commit', '-m', 'Initial commit by TOAI release agent'], cwd=repo_dir)

    # Fetch git log
    git_log = run_command(['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'], cwd=repo_dir)
    
    # Scan whitepapers or documentation if available
    docs_dir = os.path.join(repo_dir, 'docs')
    whitepaper_content = ""
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    wp_path = os.path.join(root, file)
                    try:
                        with open(wp_path, 'r', encoding='utf-8') as f:
                            whitepaper_content += f"\n--- File: {file} ---\n" + f.read()[:500]
                    except Exception as e:
                        print(f"Failed to read {wp_path}: {e}")

    summary_data = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "git_log": git_log,
        "whitepaper_snippet": whitepaper_content[:2000],
        "version": "1.0.0"
    }

    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
