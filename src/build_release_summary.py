import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_logs():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI_Generated', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:500] + "... [truncated]"
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = get_git_logs()
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_file = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Release summary successfully generated at {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
