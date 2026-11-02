import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=10):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_path):
    whitepaper_paths = [
        os.path.join(workspace_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(workspace_path, 'WHITEPAPER.md')
    ]
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.splitlines()
                    return lines[:20]
            except Exception as e:
                return [f"Failed to read whitepaper: {str(e)}"]
    return ["No whitepaper found."]

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("Scanning repository and whitepaper for release summary...")
    
    git_logs = get_git_log(repo_path)
    whitepaper_snippet = scan_whitepaper(workspace_dir)
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": git_logs,
        "whitepaper_overview": whitepaper_snippet
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
