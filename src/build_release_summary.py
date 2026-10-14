import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {e}"

def generate_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = run_git_log()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary_data = {
        "timestamp": timestamp,
        "git_recent_commits": logs,
        "version": "1.0.0",
        "status": "stable",
        "message": "Gaia Ecosystem Release Summary Generated Successfully."
    }
    
    output_file = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=4)
        
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
