import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log not available: {e}"

def scan_whitepaper(base_dir):
    whitepaper_path = os.path.join(base_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                return lines[0] if lines else "Whitepaper empty"
        except Exception as e:
            return f"Error reading whitepaper: {e}"
    return "Whitepaper not found"

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_history = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace)
    
    release_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "whitepaper_title": whitepaper_summary,
        "recent_commits": git_history.splitlines()
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        print(f"Failed to save release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
