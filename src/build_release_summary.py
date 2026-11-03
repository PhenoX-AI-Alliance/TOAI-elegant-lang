import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return ["No git repository found at specified path."]
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'WHITE_PAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content[:1000] + "... [Truncated]"
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print("Scanning git logs and ecosystem documents...")
    logs = get_git_log(repo_path)
    whitepaper_summary = scan_whitepaper(workspace)
    
    summary_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "recent_commits": logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    main()
