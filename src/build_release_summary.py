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
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000] # Return first 1000 chars as summary
            except Exception as e:
                return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_log = get_git_log()
        whitepaper_summary = scan_whitepaper()
        
        release_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_log,
            "whitepaper_summary": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built and saved to {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
