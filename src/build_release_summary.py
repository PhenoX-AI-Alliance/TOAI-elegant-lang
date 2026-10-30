import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(repo_path, max_count=10):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper(repo_path):
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Return first 500 characters as summary
                return content[:500] + "..."
        except Exception as e:
            print(f"Warning: Could not read whitepaper: {e}")
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print(f"Error: {repo_path} is not a git repository.")
        sys.exit(1)
        
    print("Scanning repository and whitepaper for release summary...")
    commits = get_git_log(repo_path)
    whitepaper_summary = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "recent_commits": commits,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
