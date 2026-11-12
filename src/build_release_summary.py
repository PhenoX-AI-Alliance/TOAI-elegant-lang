import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

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
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {{e}}", file=sys.stderr)
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_dir):
        print(f"Error: Repository directory not found at {{repo_dir}}", file=sys.stderr)
        sys.exit(1)
        
    git_dir = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_dir):
        print("Initializing git repository for build summary...", file=sys.stdout)
        subprocess.run(["git", "init"], cwd=repo_dir, check=True)
        subprocess.run(["git", "config", "user.name", "TOAI Release Bot"], cwd=repo_dir, check=True)
        subprocess.run(["git", "config", "user.email", "bot@toai.internal"], cwd=repo_dir, check=True)
        
    # Check if HEAD exists
    head_exists = True
    try:
        subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        head_exists = False
        
    if not head_exists:
        # Create an initial commit if HEAD is missing
        readme_path = os.path.join(repo_dir, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write("# TOAI Elegant Lang\nInitialized by build_release_summary.py\n")
        subprocess.run(["git", "add", "README.md"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit for release summary"], cwd=repo_dir, check=True)

    git_log = run_git_command(["git", "log", "-n", "10", "--oneline"], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, "WHITE_PAPER.md")
    whitepaper_content = "White paper not found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, "r", encoding="utf-8") as f:
            whitepaper_content = f.read()[:500] # preview first 500 chars

    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_log": git_log,
        "whitepaper_preview": whitepaper_content
    }

    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {{output_path}}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
