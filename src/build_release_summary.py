import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_logs():
    try:
        cmd = ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_workspace():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    white_paper_path = os.path.join(workspace_dir, 'WHITE_PAPER.md')
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "white_paper_exists": os.path.exists(white_paper_path),
        "git_logs": get_git_logs()
    }
    return summary

def main():
    try:
        summary = scan_workspace()
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
