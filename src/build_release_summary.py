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
        return result.stdout.strip()
    except Exception as e:
        return f"Git log acquisition failed: {str(e)}"

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'docs', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:500] + "... [Truncated]"
        except Exception as e:
            return f"Failed to read whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_logs()
        whitepaper_summary = scan_whitepaper(workspace_dir)
        
        release_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0",
            "git_logs": git_logs,
            "whitepaper_summary": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
