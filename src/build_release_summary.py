import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        cmd = ['git', 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [line.strip() for line in lines[:10] if line.strip()]
        except Exception as e:
            return [f"Failed to read whitepaper: {str(e)}"]
    return ["Whitepaper not found."]

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_commits = get_git_log()
        whitepaper_summary = scan_whitepaper(workspace_dir)
        
        release_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0-alpha",
            "git_recent_commits": git_commits,
            "whitepaper_highlights": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
