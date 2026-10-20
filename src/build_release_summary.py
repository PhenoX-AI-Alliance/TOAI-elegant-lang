import sys
import os
import traceback
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                return lines[:15]
        except Exception as e:
            return [f"Failed to read whitepaper: {str(e)}"]
    return ["Whitepaper not found."]

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "git_recent_commits": git_logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    summary_file_path = os.path.join(output_dir, 'release_summary.json')
    try:
        with open(summary_file_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {summary_file_path}")
    except Exception as e:
        print(f"Error writing release summary: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
