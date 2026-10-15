import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def generate_release():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(target_dir, exist_ok=True)
    
    git_log = "No git history"
    try:
        res = subprocess.run(['git', 'log', '-n', '20', '--oneline'], capture_output=True, text=True, cwd=workspace_dir)
        if res.returncode == 0:
            git_log = res.stdout
    except Exception as e:
        git_log = str(e)
        
    payload = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_history": git_log,
        "status": "success",
        "message": "Gaia Ecosystem release summary built with care and precision."
    }
    
    out_path = os.path.join(target_dir, 'release_report.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print("Release summary successfully built at:", out_path)

if __name__ == '__main__':
    try:
        generate_release()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
