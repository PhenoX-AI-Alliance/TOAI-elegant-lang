import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log():
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
        return f"Git log retrieval failed: {str(e)}"

def generate_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'src')
    os.makedirs(target_dir, exist_ok=True)
    
    git_history = run_git_log()
    timestamp = datetime.now().isoformat()
    
    summary_data = {
        "timestamp": timestamp,
        "version": "1.0.0",
        "recent_commits": git_history.splitlines() if git_history else []
    }
    
    output_path = os.path.join(target_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
