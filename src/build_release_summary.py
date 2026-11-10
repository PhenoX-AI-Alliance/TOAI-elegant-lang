import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        res = subprocess.run(
            ['git', '-C', repo_dir, 'log', '-n', '10', '--pretty=format:%h - %an, %ar: %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:500] + "... [truncated]"
        except Exception as e:
            return f"Failed to read whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    try:
        print("Starting release summary build...")
        git_logs = get_git_log()
        whitepaper_summary = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "git_recent_commits": git_logs.splitlines(),
            "whitepaper_excerpt": whitepaper_summary
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
