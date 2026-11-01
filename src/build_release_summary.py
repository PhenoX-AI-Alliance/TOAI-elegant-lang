import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        res = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {e}"

def generate_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'src')
    os.makedirs(target_dir, exist_ok=True)
    
    output_path = os.path.join(target_dir, 'release_summary.json')
    
    git_history = get_git_log()
    timestamp = datetime.now().isoformat()
    
    summary_data = {
        "timestamp": timestamp,
        "version": "1.0.0",
        "git_recent_commits": git_history.splitlines() if git_history else [],
        "status": "success",
        "message": "Release summary successfully built from ecosystem state."
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary generated at: {output_path}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
