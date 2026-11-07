import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log():
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def generate_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    timestamp = datetime.datetime.now().isoformat()
    
    summary_data = {
        "timestamp": timestamp,
        "git_recent_commits": git_logs,
        "release_status": "stable",
        "message": "Gaia Ecosystem release summary generated successfully."
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated release summary at: {output_file}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
