import sys
import os
import traceback
import subprocess
import datetime
import json

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

def generate_release_summary():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_history = get_git_log()
        timestamp = datetime.datetime.now().isoformat()
        
        summary_data = {
            "timestamp": timestamp,
            "version": "1.0.0",
            "git_recent_commits": git_history,
            "status": "success",
            "message": "Release summary successfully generated from repository logs."
        }
        
        out_path = os.path.join(output_dir, 'release_summary.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {out_path}")
    except Exception as e:
        print(f"Error in generate_release_summary: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    generate_release_summary()
