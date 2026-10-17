# -*- coding: utf-8 -*-
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
        return f"Git log retrieval failed: {e}"

def generate_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_history = get_git_log()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary_data = {
        "timestamp": timestamp,
        "project": "TOAI-elegant-lang",
        "recent_git_history": git_history.splitlines(),
        "status": "release summary built successfully with altruistic warmth"
    }
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
