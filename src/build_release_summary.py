import sys
import os
import traceback
import subprocess
import json
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
        return [f"Git log retrieval failed: {str(e)}"]

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'releases')
    os.makedirs(output_dir, exist_ok=True)
    
    logs = get_git_log()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_data = {
        "timestamp": timestamp,
        "git_recent_commits": logs,
        "status": "success",
        "message": "Release summary successfully generated from git history."
    }
    
    output_file = os.path.join(output_dir, f"release_summary_{timestamp}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
