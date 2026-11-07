import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                return f.read()[:1000] # return first 1000 chars as summary
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "No WHITEPAPER.md found."

def main():
    try:
        default_ws = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', default_ws)
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        print(f"Scanning repository at: {repo_path}")
        
        logs = get_git_log(repo_path)
        whitepaper_summary = scan_whitepaper(repo_path)
        
        release_data = {
            "timestamp": datetime.now().isoformat(),
            "version_summary": "TOAI Elegant Lang Release Candidate",
            "whitepaper_excerpt": whitepaper_summary,
            "recent_commits": logs
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=4)
            
        print(f"Release summary successfully built at: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
