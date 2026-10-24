import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_logs():
    try:
        res = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return "".join(lines[:20])
        except Exception as e:
            return f"Failed to read whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'releases')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = get_git_logs()
    wp_summary = scan_whitepaper(workspace_dir)
    
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_data = {
        "timestamp": now,
        "git_logs": logs,
        "whitepaper_excerpt": wp_summary
    }
    
    output_file = os.path.join(output_dir, f"release_summary_{now}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
