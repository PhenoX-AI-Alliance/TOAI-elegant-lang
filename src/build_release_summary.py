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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {e}"

def generate_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(target_dir, exist_ok=True)
    
    git_history = get_git_log()
    current_time = datetime.datetime.now().isoformat()
    
    summary_data = {
        "timestamp": current_time,
        "release_summary": "TOAI Elegant Lang Release Summary - Autonomous Generation",
        "git_recent_commits": git_history,
        "status": "stable"
    }
    
    out_file = os.path.join(target_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated release summary at {out_file}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
