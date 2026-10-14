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
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace):
    whitepaper_path = os.path.join(workspace, 'TOAI_Generated', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:500] + "..." if len(content) > 500 else content
        except Exception as e:
            return f"Failed to read whitepaper: {str(e)}"
    return "No whitepaper found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "git_history": git_logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at {output_path}")
    except Exception as e:
        print(f"Failed to write release summary: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
