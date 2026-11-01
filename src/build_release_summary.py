import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ad : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Failed to fetch git logs: {e}")
        return []

def scan_whitepaper(repo_path):
    whitepaper_paths = [
        os.path.join(repo_path, 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'CONSTITUTION.md')
    ]
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:2000] # Return first 2000 chars as summary
            except Exception as e:
                print(f"Warning: Failed to read {path}: {e}")
    return "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("Initializing git repository for TOAI-elegant-lang...")
        try:
            subprocess.run(['git', 'init', repo_path], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.name', 'TOAI Executor'], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.email', 'executor@toai.internal'], check=True)
        except Exception as e:
            print(f"Error initializing git: {e}")

    git_logs = get_git_logs(repo_path)
    whitepaper_snippet = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "git_logs": git_logs,
        "whitepaper_summary": whitepaper_snippet
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        print(f"Error writing release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
