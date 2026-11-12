import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ad : %s'],
            capture_output=True,
            text=True,
            check=True,
            cwd=os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_files = []
    try:
        for root, dirs, files in os.walk(workspace):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    wp_files.append(os.path.join(root, file))
    except Exception as e:
        pass
    return wp_files[:5]

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    summary_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    logs = get_git_log()
    whitepapers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "recent_commits": logs,
        "whitepapers_found": whitepapers
    }
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"Release summary successfully generated at: {summary_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
