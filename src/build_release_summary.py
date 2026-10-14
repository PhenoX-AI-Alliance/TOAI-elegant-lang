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
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_history = get_git_log()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "project": "TOAI-elegant-lang",
        "git_recent_commits": git_history.splitlines(),
        "status": "release_summary_generated_successfully"
    }
    
    out_path = os.path.join(output_dir, 'release_summary.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {out_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
