import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def run_git_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.getcwd())
        return result.stdout.strip()
    except Exception as e:
        print(f"Git command failed: {e}")
        return ""

def main():
    print("Initializing Release Summary Builder...")
    
    git_log = run_git_command(["git", "log", "-n", "10", "--oneline"])
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary_data = {
        "timestamp": current_date,
        "recent_commits": git_log.splitlines() if git_log else []
    }
    
    output_path = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated', 'release_summary.json')
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=4)
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        print(f"Failed to write release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
