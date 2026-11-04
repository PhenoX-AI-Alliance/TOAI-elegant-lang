import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not found. No commit history available."
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
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    potential_paths = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITEPAPER.md')
    ]
    for path in potential_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000] # Return first 1000 chars as summary
            except Exception as e:
                return f"Found whitepaper but failed to read: {str(e)}"
    return "Whitepaper not found in standard locations."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_history = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    now = datetime.datetime.now().isoformat()
    
    summary_data = {
        "timestamp": now,
        "version": "1.0.0-gaia",
        "git_log": git_history,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        print(f"Error writing release summary: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)