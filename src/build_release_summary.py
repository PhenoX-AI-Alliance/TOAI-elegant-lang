import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git logs: {e}")
        return []

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return "".join(lines[:20])
        except Exception as e:
            print(f"Warning: Could not read whitepaper: {e}")
    return "Whitepaper not found or unreadable."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = get_git_logs()
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_summary": whitepaper_summary,
        "status": "success"
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
