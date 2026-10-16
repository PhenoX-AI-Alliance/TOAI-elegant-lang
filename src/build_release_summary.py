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
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def generate_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = get_git_log()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "recent_commits": logs,
        "message": "Gaia Ecosystem Release Summary Generated Successfully."
    }
    
    output_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
