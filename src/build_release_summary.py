import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not initialized."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000] # Return first 1000 chars as summary
            except Exception as e:
                return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    print("Building release summary...")
    git_logs = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    summary_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_logs": git_logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=4)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    main()
