# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def generate_release_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    summary_path = os.path.join(output_dir, 'release_summary.json')
    
    logs = get_git_log()
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "recent_commits": logs,
        "ecosystem": "Gaia Ecosystem - Earth of Life"
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {summary_path}")

if __name__ == '__main__':
    try:
        generate_release_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
