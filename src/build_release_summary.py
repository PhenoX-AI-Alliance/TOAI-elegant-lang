import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not initialized."
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--oneline']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper(repo_path):
    possible_paths = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'src', 'WHITEPAPER.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:2000] # return first 2000 chars as summary
            except Exception as e:
                return f"Error reading whitepaper at {path}: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print("[*] Scanning git log and whitepaper...")
    git_logs = get_git_log(repo_path)
    whitepaper_summary = scan_whitepaper(repo_path)
    
    release_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_logs": git_logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_path = os.path.join(repo_path, 'src', 'release_summary.json')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
        print(f"[+] Release summary successfully written to {output_path}")
    except Exception as e:
        print(f"[-] Failed to write release summary: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
