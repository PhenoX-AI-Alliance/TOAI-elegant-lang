import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log():
    try:
        cmd = ['git', 'log', '-n', '10', '--oneline']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_workspace():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": get_git_log(),
        "workspace": workspace_dir,
        "status": "success"
    }
    return summary_data

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        summary = scan_workspace()
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
