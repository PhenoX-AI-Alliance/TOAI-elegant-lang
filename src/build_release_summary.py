import sys
import os
import traceback
import subprocess
import datetime
import json

def run_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    summary_file = os.path.join(output_dir, 'release_summary.json')
    
    commits = run_git_log()
    
    data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": commits,
        "status": "success"
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {summary_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
