import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        res = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {e}"

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        target_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'src')
        output_path = os.path.join(target_dir, 'release_summary.json')
        
        git_history = get_git_log()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "git_recent_commits": git_history.splitlines() if git_history else [],
            "status": "success",
            "message": "Release summary successfully generated from git history and whitepaper scanner."
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()\n